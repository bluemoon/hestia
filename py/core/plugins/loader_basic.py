from helpers import *
from loader import loader

class loader_basic(loader):
    def __init__(self, manager=None):
        if manager is None:
            manager = instance()
        plugins = manager.getPlugins()
        self.__plugins = plugins
    
    def __getattr__(self, name):
        if name in self.__plugin_caps:
            return _Method(self.__request, name)
        elif name in self.__interface_caps:
            raise NotImplementedError()
        else:
            return getattr(self.__plugin, name)

    def __request(self, meth, *args):
        return getattr(self.__plugins, meth)(*args)
    
    def __repr__(self):
        return ("<Loader for %s>" % (self.__plugins))
    
    __str__ = __repr__
