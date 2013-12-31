import sublime, sublime_plugin, re

class TrelloCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.settings = sublime.load_settings("Trello.sublime-settings")

    def show_quick_panel(self, items, on_done = None, on_highlighted = None, selected_index = -1):
        self.view.window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, selected_index, on_highlighted)
