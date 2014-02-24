try:
    from executable import Executable
    from card_options import CardOptions
    from custom_actions import CustomActions
except ImportError:
    from .executable import Executable
    from .card_options import CardOptions
    from .custom_actions import CustomActions

class BaseOperation(Executable):
    def __init__(self, trello_element, previous_operation = None):
        self.custom_actions = CustomActions(self)
        self.trello_element = trello_element
        self.previous_operation = previous_operation

    def names(self):
        self.set_collection()
        return self.custom_actions.encapsulate([element.name for element in self.collection])

    def trello_element_name(self):
        return self.__class__.__name__.replace("Operation", "")

    def set_collection(self):
        if hasattr(self.trello_element, self.trello_element_property()):
            self.collection = getattr(self.trello_element, self.trello_element_property())

    def trello_element_property(self):
        return ""

    def callback(self, index):
        if self.custom_actions.has(index):
            self.custom_actions.call(index)
        else:
            self.execute_command(index - self.custom_actions.len())

    def get_name(self):
        self.command.input("Name", self.add)

    def add(self, text = None):
        pass

    def execute_command(self, index):
        if self.collection_has(index):
            Operation = self.next_operation_class()
            Operation(self.find(index), self).execute(self.command)

    def collection_has(self, index):
        return len(self.collection) > index

    def next_operation_class(self):
        pass

    def find(self, index):
        return self.collection[index]

class BoardOperation(BaseOperation):
    def __init__(self, trello_element, previous_operation = None):
        super().__init__(trello_element, previous_operation)
        self.custom_actions.remove("..")

    def trello_element_property(self):
        return "boards"

    def next_operation_class(self):
        return ListOperation

    def add(self, text = None):
        if text:
            self.trello_element.add_board(text)

class ListOperation(BaseOperation):
    def trello_element_property(self):
        return "lists"

    def next_operation_class(self):
        return CardOperation

    def add(self, text = None):
        if text:
            self.trello_element.add_list(text)

class CardOperation(BaseOperation):
    def trello_element_property(self):
        return "cards"

    def next_operation_class(self):
        return CardOptions

    def add(self, text = None):
        if text:
            self.trello_element.add_card(text)