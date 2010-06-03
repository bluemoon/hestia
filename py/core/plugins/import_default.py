from import_builtin     import BuiltinPluginManager
#from import_entrypoint  import EntryPointPluginManager
#from import_directory   import DirectoryPluginManager
#from import_shell       import ShellPluginManager

class DefaultPluginManager(BuiltinPluginManager):
    name = "default"

    def __init__(self, plugins=(), config={}):
        BuiltinPluginManager.__init__(self, plugins, config)
        #EntryPointPluginManager.__init__(self, plugins, config)
        #DirectoryPluginManager.__init__(self, plugins, config)
        #ShellPluginManager.__init__(self, plugins, config)

    def loadPlugins(self):
        BuiltinPluginManager.loadPlugins(self)
        #EntryPointPluginManager.loadPlugins(self)
        #DirectoryPluginManager.loadPlugins(self)
        #ShellPluginManager.loadPlugins(self)
