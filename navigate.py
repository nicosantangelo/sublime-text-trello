from .trello import TrelloCommand

class TrelloNavigateCommand(TrelloCommand):
    def work(self, edit):
        self.boards = self.conn.me.boards
        self.show_quick_panel(self.names_from(self.boards), self.show_lists)

    # TODO: DRY!
    def show_lists(self, index):
        self.lists = self.boards[index].lists
        self.show_quick_panel(self.names_from(self.lists), self.show_cards)

    def show_cards(self, index):
        self.cards = self.lists[index].cards
        self.show_quick_panel(self.names_from(self.cards), self.show_card_options)

    def show_card_options(self, index):
        self.card_options = ["Archive", "Another option...", "Exit"]
        card = self.cards[index]

        def do_card_option(index):
            if index == 0:
                card.close()

        self.show_quick_panel(self.card_options, do_card_option)

    def names_from(self, collection):
        return [element.name for element in collection]
