class Executable():
    def execute(self, command):
        self.command = command
        self.command.display(self.names(), self.callback)

    def names(self):
        return [""]

    def callback(self):
        pass