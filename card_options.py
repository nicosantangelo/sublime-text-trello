class CardOptions():
    def __init__(self, card):
        self.options = [{
            'name': "Archive",
            'action': self.close
        }, {
            'name': "Exit",
            'action': self.noop
        }]
        self.card = card

    def names(self):
        return [option['name'] for option in self.options]

    def execute(self, index):
        option = self.options[index]
        if not option is None:
            option['action']()

    def close(self):
        self.card.close()

    def noop(self):
        pass