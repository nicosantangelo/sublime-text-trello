from executable import Executable
from card_options import CardOptions

class BaseOperation(Executable):
    def __init__(self, trello_element, previous_operation = None):
        self.trello_element = trello_element
        self.previous_operation = previous_operation

    def names(self):
        self.set_collection()
        return [".."] + [element.name for element in self.collection] + ["Exit"]

    def set_collection(self):
        if hasattr(self.trello_element, self.trello_element_property()):
            self.collection = getattr(self.trello_element, self.trello_element_property())

    def find(self, index):
        return self.collection[index]

    def trello_element_property(self):
        return ""

    def callback(self, index):
        if index == 0:
            self.go_back()
        else:
            self.execute_command(index - 1)

    def execute_command(self, index):
        if self.in_collection_range(index):
            Operation = self.next_operation_class()
            Operation(self.find(index), self).execute(self.command)

    def in_collection_range(self, index):
        return len(self.collection) > index

    def next_operation_class(self):
        pass

class BoardOperation(BaseOperation):
    def trello_element_property(self):
        return "boards"

    def names(self):
        names = super().names() 
        names.remove("..")
        return names

    def callback(self, index):
        self.execute_command(index)

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