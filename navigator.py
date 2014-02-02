from operations import *
from card_options import CardOptions

class Navigator():
    def __init__(self, receiver):
        self.receiver = receiver

    def start(self, value):
        self.show_boards(value)

    def show_boards(self, value):
        self.show(BoardOperation(value), self.show_lists)

    def show_lists(self, index):
        self.show(ListOperation(self.last_trello_element(index)), self.show_cards)

    def show_cards(self, index):
        self.show(CardOperation(self.last_trello_element(index)), self.show_card_options)

    def show_card_options(self, index):
        card = self.last_trello_element(index)
        card_options = CardOptions(card, self.receiver)

        self.receiver.execute(card_options.names(), card_options.call_action)

    def show(self, operation, callback):
        self.last_operation = operation
        self.receiver.execute(operation.element_names(), callback)

    def last_trello_element(self, index):
        return self.last_operation.find(index)