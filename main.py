import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

class AgentUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.api_key_input = TextInput(hint_text="Paste your NVIDIA API key (nvapi-...)", size_hint_y=0.1, password=True)
        self.goal_input = TextInput(hint_text="What do you want the agent to do?", size_hint_y=0.15)
        run_btn = Button(text="Run Agent", size_hint_y=0.1)
        run_btn.bind(on_press=self.run_agent)

        self.output_label = Label(text="Output will appear here...", size_hint_y=None, halign="left", valign="top")
        self.output_label.bind(width=lambda *x: self.output_label.setter("text_size")(self.output_label, (self.output_label.width, None)))
        scroll = ScrollView(size_hint_y=0.65)
        scroll.add_widget(self.output_label)

        self.add_widget(self.api_key_input)
        self.add_widget(self.goal_input)
        self.add_widget(run_btn)
        self.add_widget(scroll)

    def run_agent(self, instance):
        api_key = self.api_key_input.text.strip()
        goal = self.goal_input.text.strip()
        if not api_key or not goal:
            self.output_label.text = "Need both an API key and a goal."
            return

        self.output_label.text = "Thinking..."
        try:
            response = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-oss-120b",
                    "messages": [{"role": "user", "content": goal}],
                    "max_tokens": 1000,
                },
                timeout=30,
            )
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            self.output_label.text = text
        except Exception as e:
            self.output_label.text = f"Error: {e}"

class ClaudeAgentApp(App):
    def build(self):
        return AgentUI()

if __name__ == "__main__":
    ClaudeAgentApp().run()
