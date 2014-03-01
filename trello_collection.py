class TrelloCollection():
    def __init__(self, trello_element, attr = ""):
        if hasattr(trello_element, attr):
            self.elements = getattr(trello_element, attr)
        else:
            self.elements = trello_element

    def has(self, index):
        return len(self.elements) > index and index >= 0

    def find(self, index):
        return self.elements[index]

    def names(self):
        return [element.name for element in self.elements]