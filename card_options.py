from executable import Executable

class CardOptions(Executable):
    def __init__(self, card):
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

    def names(self):
        return [option['name'] for option in self.options]

    def callback(self, index):
        option = self.options[index]
        if not option is None:
            option['action']()

    # Actions
    def comments(self):
        self.command.display(self.card.comments())

    def comment(self, text = ""):
        if text:
            self.card.add_comment(text)
        else:
            self.command.input("Comment text", self.comment)

    def close(self):
        self.card.close()

    def noop(self):
        pass