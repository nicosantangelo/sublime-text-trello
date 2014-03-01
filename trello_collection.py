class TrelloCollection():
    def __init__(self, trello_element, attr = ""):
        if hasattr(trello_element, attr):
            elements = getattr(trello_element, attr)
        else:
            elements = trello_element
            
        self.elements = list(filter(self.not_closed, elements))

    def not_closed(self, element):
        return not element.closed

    def has(self, index):
        return len(self.elements) > index and index >= 0

    def find(self, index):
        return self.elements[index]

    def names(self):
        return [element.name for element in self.elements]