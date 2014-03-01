try:
    from executable import Executable
    from trello_collection import TrelloCollection
    from card_options import CardOptions
    from custom_actions import CustomActions
except ImportError:
    from .executable import Executable
    from .trello_collection import TrelloCollection
    from .card_options import CardOptions
    from .custom_actions import CustomActions

class BaseOperation(Executable):
    def __init__(self, trello_element, previous_operation = None):
        self.custom_actions = CustomActions(self)
        self.trello_element = trello_element
        self.previous_operation = previous_operation

    def items(self):
        self.set_collection()
        return self.custom_actions.encapsulate(self.collection.names())

    def set_collection(self):
        self.collection = TrelloCollection(self.trello_element, self.trello_element_property())

    def trello_element_property(self):
        return ""
        
    def trello_element_name(self):
        return self.__class__.__name__.replace("Operation", "")

    def callback(self, index):
        if self.custom_actions.has(index):
            self.custom_actions.call(index)
        else:
            self.execute_command(index - self.custom_actions.len())

    def get_name(self):
        self.command.input("Name", self.deferred_add)

    def deferred_add(self, text = None):
        if text:
            self.command.defer(lambda: self.base_add(text))

    def base_add(self, text):
        self.add(text)
        self.trello_element.reload()

    def add(self, text):
        pass

    def execute_command(self, index):
        if self.collection.has(index):
            Operation = self.next_operation_class()
            Operation(self.collection.find(index), self).execute(self.command)

    def next_operation_class(self):
        pass

class BoardOperation(BaseOperation):
    def __init__(self, trello_element, previous_operation = None):
        super().__init__(trello_element, previous_operation)
        self.custom_actions.remove("..")

    def trello_element_property(self):
        return "boards"

    def next_operation_class(self):
        return ListOperation

    def add(self, text):
        self.trello_element.add_board(text)

class ListOperation(BaseOperation):
    def trello_element_property(self):
        return "lists"

    def next_operation_class(self):
        return CardOperation

    def add(self, text):
        self.trello_element.add_list(text)

class CardOperation(BaseOperation):
    def trello_element_property(self):
        return "cards"

    def next_operation_class(self):
        return CardOptions

    def add(self, text):
        self.trello_element.add_card(text)