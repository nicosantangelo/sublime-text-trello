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

    def output(self, text):
        self.show_output_panel(text)

    def output_in_tab(self, text):
        self.show_in_tab(text)

    def output_editable(self, text, extra = None):
        self.show_in_editable_tab(text, extra)

    def input(self, label, callback = None):
        self.show_input_panel(label, "", callback)