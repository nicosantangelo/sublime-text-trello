try:
    from trello import TrelloCommand
    from trello_cache import TrelloCache
    from operations import BoardOperation, CardOperation
except ImportError:
    from .trello import TrelloCommand
    from .trello_cache import TrelloCache
    from .operations import BoardOperation, CardOperation

class Navegable():
    def display(self, names, callback = None):
        self.show_quick_panel(names, callback)

    def input(self, label, callback = None):
        self.show_input_panel(label, "", callback)

    def output(self, text):
        if self.results_in_new_tab:
            self.show_in_tab(text)
        else:
            self.show_output_panel(text)

    def output_editable(self, text, extra = None):
        self.show_in_editable_tab(text, extra)

class TrelloNavigateCommand(TrelloCommand, Navegable):
    def work(self, connection):
        BoardOperation(connection.me).execute(self)

class TrelloQuickCreateCardCommand(TrelloCommand, Navegable):
    def work(self, connection):
        if TrelloCache.is_empty():
            self.show_output_panel("No list on cache")
        else:
            list = TrelloCache.get() 
            operation = CardOperation(list)
            operation.command = self
            operation.get_name(label="Card name (on list %s/%s)" % (list.board.name, list.name))
            
class TrelloCreateCardWithDescriptionCommand(TrelloCommand, Navegable):
    def work(self, connection):
        if TrelloCache.is_empty():
            self.show_output_panel("No list on cache")
        else:
            list = TrelloCache.get() 
            operation = CardOperation(list)
            operation.command = self
            operation.create_with_description(label="[List %s/%s]. " % (list.board.name, list.name))
