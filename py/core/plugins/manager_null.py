class NullPluginManager(object):
    """Null plugin manager that has no plugins.
    """
    name = "null"

    def __init__(self, plugins=(), config={}):
        self.__plugins = ()

    def __iter__(self):
        return ()

    def addPlugin(self, plug):
        raise NotImplementedError()

    def addPlugins(self, plugins):
        raise NotImplementedError()

    def delPlugin(self, plug):
        raise NotImplementedError()

    def delPlugins(self, plugins):
        raise NotImplementedError()

    def getPlugins(self, name=None, interface=None):
        return ()

    def _get_plugins(self):
        return self.__plugins

    plugins = property(_get_plugins, None, None,
                       """Access the list of plugins managed by
                       this plugin manager""")
