__author__ = 'herve.beraud'
import sys
import os
from core import colors
from core import settings
import plugins
import pkgutil

__all__ = []

class Plugins(list):
    path = os.path.join(settings.BASE_DIR, "plugins")

    def __init__(self):
        list.__init__(self)
        self.load()

    def load(self):
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):
            if not ispkg:
                self.append(modname)
                __all__.append(modname)

    def display(self):
        msg = "[+] Available plugins:"
        print(colors.green(msg))
        print(colors.green("-" * len(msg)))

        for module in self:
            print(module)
        sys.exit(1)


#def available():
#    path = "plugins/"
#    msg = "[+] Available plugins:"
#    print(colors.green(msg))
#    print(colors.green("-" * len(msg)))
#    sys.path.insert(0, path)
#    for f in os.listdir(path):
#        fname, ext = os.path.splitext(f)
#        if ext == '.py':
#            print(fname)
#    sys.exit(1)