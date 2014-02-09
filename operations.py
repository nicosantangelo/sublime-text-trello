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

class BoardOperation(BaseOperation):
    def callback(self, index):
        ListOperation(self.find(index)).execute(self.command)

    def trello_element_property(self):
        return "boards"

class ListOperation(BaseOperation):
    def callback(self, index):
        CardOperation(self.find(index)).execute(self.command)

    def trello_element_property(self):
        return "lists"

class CardOperation(BaseOperation):
    def callback(self, index):
        CardOptions(self.find(index)).execute(self.command)

    def trello_element_property(self):
        return "cards"