from import_base import ImportBase

class BuiltinPluginManager(ImportBase):
    def loadPlugins(self):
        import builtin_plugins
        for i in builtin_plugins.imports:
            self.add_import(i) 
