class BaseOperation():
    def __init__(self, trello_element = None):
        self.trello_element = trello_element

    def set_collection(self):
        self.collection = getattr(self.trello_element, self.collection_name)

    def find(self, index):
        return self.collection[index]

    def element_names(self):
        self.set_collection()
        return self.names()

    def names(self):
        return [element.name for element in self.collection]

class BoardOperation(BaseOperation):
    @property
    def collection_name(self):
        return "boards"

class ListOperation(BaseOperation):
    @property
    def collection_name(self):
        return "lists"

class CardOperation(BaseOperation):
    @property
    def collection_name(self):
        return "cards"