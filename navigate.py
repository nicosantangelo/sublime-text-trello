from .trello import TrelloCommand

class TrelloNavigateCommand(TrelloCommand):
    def work(self, edit):
        self.boards = self.conn.me.boards
        self.show_quick_panel(self.names_from(self.boards), self.show_cards)

    def show_cards(self, index):
        self.cards = self.boards[index].cards
        self.show_quick_panel(self.names_from(self.cards), self.card_options)

    def card_options(self, index):
        # self.cards[index].close()

    def names_from(self, collection):
        return [element.name for element in collection]
