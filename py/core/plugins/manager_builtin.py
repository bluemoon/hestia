from manager_base import PluginManager

class BuiltinPluginManager(PluginManager):
    """Plugin manager that loads plugins from the list in L{builtin}.
    """
    name = "builtin"

    def loadPlugins(self):
        """Load plugins in L{builtin}.
        """
        from pkg.plugins import builtin
        for plug in builtin.plugins:
            self._loadPlugin(plug())
