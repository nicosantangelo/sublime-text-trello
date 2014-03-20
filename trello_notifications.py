try:
    from trello import TrelloCommand
    from output import Output
except ImportError:
    from .trello import TrelloCommand
    from .output import Output

class TrelloNotificationsCommand(TrelloCommand):
    def work(self, connection):
        self.options = [
            { 'name': "Unread", 'action': self.show_unread },
            { 'name': "Read all", 'action': self.read_all },
            { 'name': "Exit", 'action': self.noop }
        ]
        self.show_quick_panel(self.items(), self.callback)

    def items(self):
        return [option['name'] for option in self.options]

    def callback(self, index):
        option = self.options[index]
        if not option is None:
            option['action']()

    def show_unread(self):
        self.view.run_command("trello_unread_notifications")

    def read_all():
        pass

    def noop():
        pass

class TrelloUnreadNotificationsCommand(TrelloCommand):
    def work(self, connection):
        member = connection.me
        output = Output.notifications(member.unread_notifications())
        self.show_output_panel(output)