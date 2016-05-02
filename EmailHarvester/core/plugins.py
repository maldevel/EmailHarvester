__author__ = 'herve.beraud'
import sys
from EmailHarvester.core.output import alert
from EmailHarvester.core.output import message
import EmailHarvester.plugins as plugins
import pkgutil

__all__ = []


class Plugins(list):
    def __init__(self):
        list.__init__(self)
        self.load()

    def load(self):
        for importer, modname, ispkg in pkgutil.iter_modules(plugins.__path__):
            if not ispkg:
                self.append(modname)
                __all__.append(modname)

    def display(self):
        alert("[+] Available plugins:", underline=True)
        for module in self:
            message(module)
        sys.exit(1)

    def execute(self, name, domain, limit, proxy, user_agent):
        return self.run(name, domain, limit, proxy, user_agent)

    def run(self, name, domain, limit, proxy, user_agent):
        plugin_path = "EmailHarvester.plugins.{0}".format(name)
        module = __import__(plugin_path, globals(), locals(), ['object'], 0)
        return module.start(domain, limit, proxy, user_agent)