import sublime, sublime_plugin, re

import sys
import os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from trollop import TrelloConnection

# A base for each command
class TrelloCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.setup_data_from_settings()
        
        if not self.token:
            print("Please go to %s and paste the token in the settings" % self.token_url())
            return

        self.conn = TrelloConnection(self.key, self.token)
        self.work(edit)

    # Main method, override
    def work(self, edit):
        pass

    def token_url(self):
        return "https://trello.com/1/connect?key=%s&name=sublime_app&response_type=token&scope=read,write" % self.settings.get("key")

    def setup_data_from_settings(self):
        default_settings = sublime.load_settings("Default_app.sublime-settings")
        user_settings    = sublime.load_settings("Trello.sublime-settings")

        self.key    = default_settings.get("key")    or user_settings.get("key")
        self.secret = default_settings.get("secret") or user_settings.get("secret")
        self.token  = user_settings.get("token")

    # Panels and message
    def display_message(self, text):
        sublime.active_window().active_view().set_status("trello", text)

    def show_quick_panel(self, items, on_done = None, on_highlighted = None, selected_index = -1):
        self.view.window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, selected_index, on_highlighted)

    def show_input_panel(self, caption, initial_text = "", on_done = None, on_change = None, on_cancel = None):
        self.view.window().show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
