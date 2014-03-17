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
    # TODO: Refactor reexecute calls
    def show(self):
        self.command.output(Output.card(self.card))
        self.reexecute()

    def comments(self):
        self.command.output(Output.comments(self.card.comments()))
        self.reexecute()

    def comment(self):
        self.run_action_with_callback("Comment text", self.card.add_comment)

    def set_label(self):
        self.run_action_with_callback(self.label_input_text(), self.card.set_label)

    def clear_label(self):
        self.run_action_with_callback(self.label_input_text(), self.card.clear_label)

    def run_action_with_callback(self, input_text, callback):
        def action(text = None):
            if text is None:
                self.command.input(input_text, action)
            else:
                self.command.defer(lambda: callback(text))
                self.card.reload()
                self.reexecute()

        action()

    def move(self, index = None):
        if index is None:
            self.list_collection = TrelloCollection(self.card.board, "lists")
            self.command.display(self.list_collection.names(), self.move)
        else:
            selected_list = self.list_collection.find(index)
            self.command.defer(lambda: self.card.move_to_list(selected_list))
            selected_list.reload()
            self.reexecute()

    def close(self):
        self.card.close()
        self.card.list.reload()
        self.reexecute()

    def noop(self):
        pass

    def label_input_text(self):
        valid_label_colors = ['green', 'yellow', 'orange', 'red', 'purple', 'blue']
        current_colors = [label['color'] for label in self.card.labels]
        available_choices = [label + ("*" if label in current_colors else "") for label in valid_label_colors]
        
        return "Colors (* is active): " + ", ".join(available_choices)