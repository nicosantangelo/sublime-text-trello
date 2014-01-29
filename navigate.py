from .trello import TrelloCommand
import operations
import card_options

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
        except (AttributeError, TypeError):
            operation = Operation(indexOrObject)

        self.last_operation = operation
        self.show_quick_panel(operation.element_names(), callback)

    def show_card_options(self, index):
        card = self.last_operation.find(index)
        card_options = CardOptions(card)

        self.show_quick_panel(card_options.names(), card_options.execute)
