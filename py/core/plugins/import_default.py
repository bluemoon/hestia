from import_builtin      import import_builtin
from import_entrypoint   import import_entrypoint
from import_directory    import import_directory

from import_base         import ImportBase

class default_import_manager(import_builtin, import_entrypoint, import_directory):
    def init(self):
        import_builtin.init(self)
        import_entrypoint.init(self)
        import_directory.init(self)

    def load_imports(self):
        import_builtin.load_imports(self)
        import_entrypoint.load_imports(self)
        import_directory.load_imports(self)
