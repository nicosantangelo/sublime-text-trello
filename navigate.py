from .trello import TrelloCommand
import operations

class TrelloNavigateCommand(TrelloCommand):
    def work(self, edit):
        self.show(BoardOperation, self.conn.me, self.show_lists)

    def show_lists(self, index):
        self.show(ListOperation, index, self.show_cards)

    def show_cards(self, index):
        self.show(CardOperation, index, self.show_card_options)

    def show(self, Operation, indexOrObject, callback):
        try:
            operation = Operation(self.last_operation.find(indexOrObject))
        except AttributeError:
            operation = Operation(indexOrObject)

        self.last_operation = operation
        self.show_quick_panel(operation.element_names(), callback)

    def show_card_options(self, index):
        self.card_options = ["Archive", "Another option...", "Exit"]
        card = self.last_operation.find(index)

        def do_card_option(index):
            if index == 0:
                card.close()

        self.show_quick_panel(self.card_options, do_card_option)