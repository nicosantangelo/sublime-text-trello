from Trello.trello import TrelloCommand
from Trello.operations import *
from Trello.card_options import CardOptions

class TrelloNavigateCommand(TrelloCommand):
    def work(self, edit):
        self.show(BoardOperation(self.conn.me), self.show_lists)

    def show_lists(self, index):
        self.show(ListOperation(self.last_trello_element(index)), self.show_cards)

    def show_cards(self, index):
        self.show(CardOperation(self.last_trello_element(index)), self.show_card_options)

    def last_trello_element(self, index):
        return self.last_operation.find(index)

    def show(self, operation, callback):
        self.last_operation = operation
        self.show_quick_panel(operation.element_names(), callback)

    def show_card_options(self, index):
        card = self.last_operation.find(index)
        card_options = CardOptions(card, self)

        self.show_quick_panel(card_options.names(), card_options.execute)