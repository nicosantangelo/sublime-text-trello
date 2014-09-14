import sublime, sublime_plugin, re

import sys, os.path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib"))
    
from progress_notifier import ProgressNotifier
from open_views import OpenViews

import trollop

# A base for each command
class TrelloCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.setup_data_from_settings()
        
        if not self.token:
            self.show_output_panel(self.help_text())
            return
            
        if not self.use_cache:
            self.view.run_command("trello_delete_cache")

        trello_connection = trollop.TrelloConnection(self.key, self.token)
        self.defer(lambda: self.work(trello_connection))

    def setup_data_from_settings(self):
        default_settings = sublime.load_settings("Default_app.sublime-settings")
        user_settings    = sublime.load_settings("Trello.sublime-settings")

        self.key    = user_settings.get("key") or default_settings.get("key")
        self.secret = user_settings.get("secret") or default_settings.get("secret")
        self.token  = user_settings.get("token")
        self.use_cache = user_settings.get("use_cache", True)
        self.renavigate = user_settings.get("keep_navigate_open_after_action", True)
        self.results_in_new_tab = user_settings.get("results_in_new_tab", True)
        self.card_delimiter = user_settings.get("card_delimiter", "<end>")
        self.syntax_file = user_settings.get("syntax_file")

    def help_text(self):
        first  = "Sorry for the interruption, in order to use the package please go to:\n%s\nand paste the token in the settings (Preferences -> Package Settings -> Trello -> Settings - User). You can check Settings - Default to see the settings structure." % self.token_url()
        middle = "If you don't want to use the default app, you can change the key and the secret too, just go to:\n%s\nand copy paste both to the settings :)" % self.key_secret_generator_url()
        last   = "For more info, you can go to: https://github.com/NicoSantangelo/sublime-text-trello"
        return "%s\n\n%s\n\n%s" % (first, middle, last)

    def token_url(self):
        return "https://trello.com/1/connect?key=%s&name=sublime_app&response_type=token&scope=read,write" % self.key

    def key_secret_generator_url(self):
        return "https://trello.com/1/appKey/generate"

    # Main method, override
    def work(self, connection):
        pass

    # Panels and message
    def display_message(self, text):
        sublime.status_message("trello: %s" % text)

    def show_quick_panel(self, items, on_done = None, on_highlighted = None, selected_index = -1):
        sublime.set_timeout(lambda: self.view.window().show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, selected_index, on_highlighted), 0)

    def show_input_panel(self, caption, initial_text = "", on_done = None, on_change = None, on_cancel = None):
        self.view.window().show_input_panel(caption, initial_text, on_done, on_change, on_cancel)

    # Output view
    def show_in_editable_tab(self, text, extra = None):
        view = self.show_in_tab(text)
        view.set_scratch(True)
        OpenViews.set(view, extra)

    def show_in_tab(self, text):
        view = self.view.window().new_file()
        view.set_name("Trello")
        view.run_command("view_insert", { "size" : view.size(), "content": text });
        self.set_new_view_attributes(view)
        return view

    def show_output_panel(self, text):
        self.output_view = self.view.window().get_output_panel("textarea")
        self.append_to_output_view(text)
        self.view.window().run_command("show_panel", { "panel": "output.textarea" })
        self.set_new_view_attributes(self.output_view)

    def append_to_output_view(self, text):
        self.output_view.set_read_only(False)
        self.output_view.run_command("append", { "characters": text })
        self.output_view.set_read_only(True)

    def set_new_view_attributes(self, view):
        view.set_syntax_file(self.syntax_file)
        view.set_viewport_position((0, 0), True)

    # Helpers
    def defer(self, fn):
        self.async(fn, 0)
        
    def async(self, fn, delay):
        progress = ProgressNotifier('Trello: Working')
        sublime.set_timeout_async(lambda: self.call(fn, progress), delay)

    def call(self, fn, progress):
        fn()
        progress.stop()

class ViewInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, size, content):
        self.view.insert(edit, size, content)

class TrelloOnClose(sublime_plugin.EventListener):
    def on_close(self, view):
        view_dict = OpenViews.get(view)
        if view_dict:
            OpenViews.remove(view)
            operation = view_dict['extra']
            content = view.substr(sublime.Region(0, view.size()))
            if content:
                operation.command.defer(lambda: operation.full_add(content))
            else:
                operation.reexecute()