from import_builtin      import import_builtin
from import_base         import ImportBase

class default_import_manager(import_builtin):
    def init(self):
        import_builtin.init(self)
        
    def load_imports(self):
        import_builtin.load_imports(self)

"""
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
"""
