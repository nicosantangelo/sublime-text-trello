class Executable():
    def execute(self, command = None):
        self.command = command or self.command
        self.command.display(self.names(), self.callback)
        return self

    def names(self):
        return [""]

    def callback(self):
        pass

    def go_back(self):
        self.previous_operation.execute()