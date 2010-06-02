class PluginManager(object):
    """Base class for plugin managers. Does not implement loadPlugins, so it
    may only be used with a static list of plugins.
    """
    name = "base"

    def __init__(self, plugins=(), config={}):
        self.__plugins = []
        if plugins:
            self.addPlugins(plugins)

    def __iter__(self):
        return iter(self.plugins)

    def addPlugin(self, plug):
        self.__plugins.append(plug)

    def addPlugins(self, plugins):
        for plug in plugins:
            self.addPlugin(plug)

    def delPlugin(self, plug):
        if plug in self.__plugins:
            self.__plugins.remove(plug)

    def delPlugins(self, plugins):
        for plug in plugins:
            self.delPlugin(plug)

    def getPlugins(self, interface=None, name=None):
        plugins = []
        for plugin in self.__plugins:
            if (interface is None or plugin.interface == interface) and \
               (name is None or plugin.name == name):
                plugins.append(plugin)
        return plugins

    def _loadPlugin(self, plug):
        if plug.required_api_version > pkg.plugins.interface.IPlugin.version:
            log.warn("version dismatch: requires %s", plug.required_api_version)
            return
        loaded = False
        for p in self.plugins:
            if p.name == plug.name and \
                p.interface == plug.interface:
                loaded = True
                break
        if not loaded:
            self.addPlugin(plug)
            log.debug("%s: loaded plugin %s implement %s", self.name, plug.name, plug.interface)

    def loadPlugins(self):
        pass

    def _get_plugins(self):
        return self.__plugins

    def _set_plugins(self, plugins):
        self.__plugins = []
        self.addPlugins(plugins)

    plugins = property(_get_plugins, _set_plugins, None,
                       """Access the list of plugins managed by
                       this plugin manager""")

