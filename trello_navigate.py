try:
    from trello import TrelloCommand
    from operations import BoardOperation
except ImportError:
    from .trello import TrelloCommand
    from .operations import BoardOperation

class TrelloNavigateCommand(TrelloCommand):
    def work(self, connection):
        BoardOperation(connection.me).execute(self)

    def display(self, names, callback = None):
        self.show_quick_panel(names, callback)

    def input(self, label, callback = None):
        self.show_input_panel(label, "", callback)

    def output(self, text):
        if self.results_in_new_tab:
            self.show_in_tab(text)
        else:
            self.show_output_panel(text)

    def output_editable(self, text, extra = None):
        self.show_in_editable_tab(text, extra)
