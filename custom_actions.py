class CustomActions():
    sufix = ["Exit"]
    
    def __init__(self, operation):
        self.prefixes = ["..", "Create " + operation.trello_element_name()]
        self.prefix_methods = [operation.go_back, operation.get_name]

    def encapsulate(self, data):
        return self.prefixes + data + self.sufix

    def call(self, index):
        return self.prefix_methods[index]()

    def has(self, index):
        return self.len() > index and index >= 0

    def len(self):
        return len(self.prefixes)

    def add(self, prefix, method):
        self.prefixes.append(prefix)
        self.prefix_methods.append(method)

    def rename(self, old_name, new_name):
        index = self.prefixes.index(old_name)
        self.prefixes[index] = new_name

    def remove(self, name):
        index = self.prefixes.index(name)
        self.prefixes.pop(index)
        self.prefix_methods.pop(index)