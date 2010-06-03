from import_builtin      import import_builtin
from import_base         import ImportBase

from container_singleton import Singleton


class default_import_manager(import_builtin):
    def load_imports(self):
        self.builtin = import_builtin()
        self.builtin.load_imports()

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
