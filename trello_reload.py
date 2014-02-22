import sys, glob, sublime_plugin
from imp import reload

class TrelloReloadCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for module_name in self.module_names():
            self.reload("Trello." + module_name)
            self.reload(module_name)

    def module_names(self):            
        return ['trollop.lib'] + [py_file[:-3] for py_file in glob.glob('*.py')]

    def reload(self, module_name):
        if module_name in sys.modules:  
            print("Reloading: " + module_name)
            reload(sys.modules[module_name])