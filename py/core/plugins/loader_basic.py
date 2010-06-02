from helpers import *
from loader import loader

class loader_basic(loader):
    def __init__(self, name, manager=None):
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
        return getattr(self.__plugin, meth)(*args)
    
class PluginProxy(object):
    """
    Proxy for plugin calls.

    Note: it only proxy for the fisrt found plugin.
    """
    def __init__(self, interface, name, manager=None):
        if manager is None:
            manager = instance()
        plugins = manager.getPlugins(interface, name)
        if not plugins:
            raise NotImplementedError()
        self.__plugin = plugins[0]
        self.__plugin_caps = self.__plugin.caps()
        self.__interface_caps = pkg.plugins.interface.get_caps(interface)

    def __request(self, meth, *args):
        return getattr(self.__plugin, meth)(*args)

    def __repr__(self):
        return ("<PluginProxy for %s>" % (self.__plugin))

    __str__ = __repr__

    def __getattr__(self, name):
        if name in self.__plugin_caps:
            return _Method(self.__request, name)
        elif name in self.__interface_caps:
            raise NotImplementedError()
        else:
            return getattr(self.__plugin, name)
