import sublime, sublime_plugin, re

import sys
import os.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))

from trollop import TrelloConnection

# A base for each command
class TrelloCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.settings = sublime.load_settings("Trello.sublime-settings")
        self.conn = TrelloConnection(self.settings.get("key"), self.settings.get("token"))
        self.work(edit)

    # Main method, override
    def work(self, edit):
        pass

    # Panels and message
    def display_message(self, text):
        sublime.active_window().active_view().set_status("trello", text)

    def show_quick_panel(self, items, on_done = None, on_highlighted = None, selected_index = -1):
        self.view.window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, selected_index, on_highlighted)

    def show_input_panel(self, caption, initial_text = "", on_done = None, on_change = None, on_cancel = None):
        self.view.window().show_input_panel(caption, initial_text, on_done, on_change, on_cancel)
