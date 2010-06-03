from import_base import PluginManager

import os

class DirectoryPluginManager(PluginManager):
    """Plugin manager that loads plugins from plugin directories.
    """
    name = "directory"

    def __init__(self, plugins=(), config={}):
        default_directory = os.path.join(os.path.dirname(
                                find_module("pkg")[1]), "pkg", "plugins")
        self.directories = config.get("directories", (default_directory,))
        PluginManager.__init__(self, plugins, config)

    def loadPlugins(self):
        """Load plugins by iterating files in plugin directories.
        """
        plugins = []
        for dir in self.directories:
            try:
                for f in os.listdir(dir):
                    if f.endswith(".py") and f != "__init__.py":
                        plugins.append((f[:-3], dir))
            except OSError:
                log.warn("Failed to access: %s", dir)
                continue

        fh = None
        mod = None
        for (name, dir) in plugins:
            try:
                acquire_lock()
                fh, filename, desc = find_module(name, [dir])
                old = sys.modules.get(name)
                if old is not None:
                    # make sure we get a fresh copy of anything we are trying
                    # to load from a new path
                    del sys.modules[name]
                mod = load_module(name, fh, filename, desc)
            finally:
                if fh:
                    fh.close()
                release_lock()
            if hasattr(mod, "__all__"):
                attrs = [getattr(mod, x) for x in mod.__all__]
                for plug in attrs:
                    if not issubclass(plug, Plugin):
                        continue
                    self._loadPlugin(plug())
