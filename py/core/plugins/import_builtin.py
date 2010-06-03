from import_base import PluginManager

class BuiltinPluginManager(PluginManager):
    """Plugin manager that loads plugins from the list in L{builtin}.
    """
    name = "builtin"

    def loadPlugins(self):
        """Load plugins in L{builtin}.
        """
        import builtin_plugins
        for plug in builtin_plugins.plugins:
            self._loadPlugin(plug())
