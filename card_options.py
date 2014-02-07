class CardOptions():
    def __init__(self, card, command):
        self.options = [{
            'name': "Comments",
            'action': self.comments
        }, {
            'name': "Comment",
            'action': self.comment
        }, {
            'name': "Archive",
            'action': self.close
        }, {
            'name': "Exit",
            'action': self.noop
        }]
        self.card = card
        self.command = command

    def names(self):
        return [option['name'] for option in self.options]

    def call_action(self, index):
        option = self.options[index]
        if not option is None:
            option['action']()

    # Actions
    def comments(self):
        self.command.show_quick_panel(self.card.comments())

    def comment(self, text = ""):
        if text:
            self.card.add_comment(text)
        else:
            self.command.show_input_panel("Text", "", self.comment)

    def close(self):
        self.card.close()

    def noop(self):
        pass