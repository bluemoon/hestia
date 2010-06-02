from manager_builtin     import BuiltinPluginManager
from manager_entrypoint  import EntryPointPluginManager
from manager_directory   import DirectoryPluginManager
from manager_shell       import ShellPluginManager

class DefaultPluginManager(BuiltinPluginManager, EntryPointPluginManager,
                           DirectoryPluginManager, ShellPluginManager):
    """Plugin manager that try to load as many plugins as possible.
    """
    name = "default"

    def __init__(self, plugins=(), config={}):
        BuiltinPluginManager.__init__(self, plugins, config)
        EntryPointPluginManager.__init__(self, plugins, config)
        DirectoryPluginManager.__init__(self, plugins, config)
        ShellPluginManager.__init__(self, plugins, config)

    def loadPlugins(self):
        BuiltinPluginManager.loadPlugins(self)
        EntryPointPluginManager.loadPlugins(self)
        DirectoryPluginManager.loadPlugins(self)
        ShellPluginManager.loadPlugins(self)
