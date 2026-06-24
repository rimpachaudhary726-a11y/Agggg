[app]
title = ClaudeAgent
package.name = claudeagent
package.domain = org.hh.claudeagent
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.accept_sdk_license = True
android.api = 33
android.minapi = 21
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
