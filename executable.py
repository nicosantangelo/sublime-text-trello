class Executable():
    def execute(self, command = None):
        self.command = command or self.command
        self.command.display(self.items(), self.callback)
        return self

    def reexecute(self):
        if self.command.renavigate:
            self.execute()

    def items(self):
        return [""]

    def callback(self):
        pass

    def go_back(self):
        self.previous_operation.execute()