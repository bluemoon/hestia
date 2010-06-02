
class EntryPointPluginManager(PluginManager):
    """Plugin manager that loads plugins from entrypoints.
    """
    name = "entrypoint"

    def __init__(self, plugins=(), config={}):
        self.entrypoints = config.get("entrypoints", ("pkg.plugins",))
        PluginManager.__init__(self, plugins, config)

    def loadPlugins(self):
        """Load plugins by iterating all entry points.
        """
        try:
            from pkg_resources import iter_entry_points
        except ImportError:
            return
        for entrypoint in self.entrypoints:
            for ep in iter_entry_points(entrypoint):
                try:
                    plug = ep.load()
                except KeyboardInterrupt:
                    raise
                except Exception, e:
                    warn("Unable to load plugin %s: %s" % (ep, e), RuntimeWarning)
                    continue
                self._loadPlugin(plug())
