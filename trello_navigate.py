from Trello.trello import TrelloCommand
from Trello.navigator import Navigator

class TrelloNavigateCommand(TrelloCommand):
    def work(self, edit):
        navigator = Navigator(self)
        navigator.start(self.conn.me)

    def execute(self, names, callback):
        self.show_quick_panel(names, callback)


