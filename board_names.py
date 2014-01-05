from .trello import TrelloCommand

class TrelloBoardNamesCommand(TrelloCommand):
    def work(self, edit):
        board_names = [board.name for board in self.conn.me.boards]
        self.show_quick_panel(board_names)