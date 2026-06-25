import threading
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

class AgentUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.api_key_input = TextInput(hint_text="Paste your Cerebras API key (csk-...)", size_hint_y=0.1, password=True)
        self.goal_input = TextInput(hint_text="What do you want the agent to do?", size_hint_y=0.15)
        self.run_btn = Button(text="Run Agent", size_hint_y=0.1)
        self.run_btn.bind(on_press=self.start_agent)

        self.output_label = Label(text="Output will appear here...", size_hint_y=None, halign="left", valign="top")
        self.output_label.bind(width=lambda *x: self.output_label.setter("text_size")(self.output_label, (self.output_label.width, None)))
        scroll = ScrollView(size_hint_y=0.65)
        scroll.add_widget(self.output_label)

        self.add_widget(self.api_key_input)
        self.add_widget(self.goal_input)
        self.add_widget(self.run_btn)
        self.add_widget(scroll)

    def start_agent(self, instance):
        api_key = self.api_key_input.text.strip()
        goal = self.goal_input.text.strip()
        if not api_key or not goal:
            self.output_label.text = "Need both an API key and a goal."
            return

        self.run_btn.disabled = True
        self.output_label.text = "Thinking..."
        threading.Thread(target=self.call_api, args=(api_key, goal), daemon=True).start()

    def call_api(self, api_key, goal):
        try:
            response = requests.post(
                "https://api.cerebras.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-oss-120b",
                    "messages": [{"role": "user", "content": goal}],
                    "max_tokens": 1000,
                },
                timeout=30,
            )
            data = response.json()
            if "choices" in data:
                result = data["choices"][0]["message"]["content"]
            else:
                result = f"API Error ({response.status_code}): {data}"
        except requests.exceptions.Timeout:
            result = "Error: Request timed out. Check your connection and try again."
        except requests.exceptions.ConnectionError:
            result = "Error: Could not connect. Check your internet connection."
        except Exception as e:
            result = f"Error: {e}"

        Clock.schedule_once(lambda dt: self.show_result(result))

    def show_result(self, result):
        self.output_label.text = result
        self.run_btn.disabled = False

class ClaudeAgentApp(App):
    def build(self):
        return AgentUI()

if __name__ == "__main__":
    ClaudeAgentApp().run()
