import sys
import sublime_plugin

from imp import reload

class TrelloDeleteCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if 'trollop' in sys.modules:  
            del(sys.modules['trollop.lib'])
            import trollop
            reload(trollop)
