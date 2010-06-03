from import_base import ImportBase

class import_builtin(ImportBase):
    def load_imports(self):
        import builtin_plugins
        for i in builtin_plugins.imports:
            self.add_import(i) 
