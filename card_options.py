try:
    from trello_collection import TrelloCollection
    from executable import Executable
    from output import Output
except ImportError:
    from .trello_collection import TrelloCollection
    from .executable import Executable
    from .output import Output

class CardOptions(Executable):
    def __init__(self, card, previous_operation = None):
        self.options = [
            { 'name': "..", 'action': self.go_back },
            { 'name': "Show", 'action': self.show },
            { 'name': "Comments", 'action': self.comments },
            { 'name': "Comment", 'action': self.comment },
            { 'name': "Add label", 'action': self.set_label },
            { 'name': "Remove label", 'action': self.clear_label },
            { 'name': "Move to another List", 'action': self.move },
            { 'name': "Archive", 'action': self.close },
            { 'name': "Exit", 'action': self.noop }
        ]
        self.card = card
        self.previous_operation = previous_operation

    def items(self):
        return [option['name'] for option in self.options]

    def callback(self, index):
        option = self.options[index]
        if not option is None:
            self.command.defer(option['action'])

    # Actions
    def show(self):
        self.command.output(Output.card(self.card))

    def comments(self):
        self.command.output(Output.comments(self.card.comments()))

    # TODO: Abstract this pattern
    def comment(self, text = None):
        if text is None:
            self.command.input("Comment text", self.comment)
        else:
            self.command.defer(lambda: self.card.add_comment(text))

    def set_label(self, color = None):
        if color is None:
            self.command.input("Label color name", self.set_label)
        else:
            self.command.defer(lambda: self.card.set_label(color))

    def clear_label(self, color = None):
        if color is None:
            self.command.input("Label color name", self.clear_label)
        else:
            self.command.defer(lambda: self.card.clear_label(color))

    def move(self, index = None):
        if index is None:
            self.list_collection = TrelloCollection(self.card.board, "lists")
            self.command.display(self.list_collection.names(), self.move)
        else:
            selected_list = self.list_collection.find(index)
            self.command.defer(lambda: self.card.move_to_list(selected_list))
            selected_list.reload()

    def close(self):
        self.card.close()
        self.card.list.reload()

    def noop(self):
        pass

