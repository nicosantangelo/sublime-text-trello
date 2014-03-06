try:
    from trello import TrelloCommand
    from output import Output
except ImportError:
    from .trello import TrelloCommand
    from .output import Output

class TrelloUnreadNotificationsCommand(TrelloCommand):
    def work(self, connection):
        member = connection.me
        output = Output.notifications(member.unread_notifications())
        self.show_output_panel(output)