class ImportManager(object):
    name = "base"
    def __init__(self, imports=(), config={}):
        self.__imports = []
        if imports:
            self.addImports(imports)

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

    def getPlugins(self, name=None):
        plugins = []
        for plugin in self.__plugins:
            if (name is None or plugin.name == name):
                plugins.append(plugin)
                
        return plugins

    def _loadPlugin(self, plug):
        if not hasattr(plug, 'required_api_version'):
            return
        if plug.required_api_version > pkg.plugins.interface.IPlugin.version:
            log.warn("version dismatch: requires %s", plug.required_api_version)
            return
        
        loaded = False
        for p in self.plugins:
            if p.name == plug.name:
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


class PluginManager(object):
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

    def getPlugins(self, name=None):
        plugins = []
        for plugin in self.__plugins:
            if (name is None or plugin.name == name):
                plugins.append(plugin)
                
        return plugins

    def _loadPlugin(self, plug):
        if not hasattr(plug, 'required_api_version'):
            return
        if plug.required_api_version > pkg.plugins.interface.IPlugin.version:
            log.warn("version dismatch: requires %s", plug.required_api_version)
            return
        
        loaded = False
        for p in self.plugins:
            if p.name == plug.name:
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

