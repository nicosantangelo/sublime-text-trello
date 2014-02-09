from executable import Executable
from card_options import CardOptions

class BaseOperation(Executable):
    def __init__(self, trello_element):
        self.trello_element = trello_element

    def names(self):
        self.set_collection()
        return [element.name for element in self.collection]

    def set_collection(self):
        if hasattr(self.trello_element, self.trello_element_property()):
            self.collection = getattr(self.trello_element, self.trello_element_property())

    def find(self, index):
        return self.collection[index]

    def trello_element_property(self):
        return ""

    def callback(self, index):
        Operation = self.next_operation_class()
        Operation(self.find(index)).execute(self.command)

    def next_operation_class(self):
        pass

class BoardOperation(BaseOperation):
    def trello_element_property(self):
        return "boards"

    def next_operation_class(self):
        return ListOperation

class ListOperation(BaseOperation):
    def trello_element_property(self):
        return "lists"

    def next_operation_class(self):
        return CardOperation

class CardOperation(BaseOperation):
    def trello_element_property(self):
        return "cards"

    def next_operation_class(self):
        return CardOptions