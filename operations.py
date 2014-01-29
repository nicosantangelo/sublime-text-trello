class BaseOperation():
    def find(self, index):
        return self.collection[index]

    def element_names(self):
        self.set_collection()
        return self.names_from(self.collection)

    def names_from(self, collection):
        return [element.name for element in collection]

class BoardOperation(BaseOperation):
    def __init__(self, user):
        self.user = user

    def set_collection(self):
        self.collection = self.user.boards

class ListOperation(BaseOperation):
    def __init__(self, board):
        self.board = board

    def set_collection(self):
        self.collection = self.board.lists

class CardOperation(BaseOperation):
    def __init__(self, lst):
        self.list = lst

    def set_collection(self):
        self.collection = self.list.cards