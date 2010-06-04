from import_base import ImportBase
import imp
import sys

builtins = (
    ("hestia.monitoring.monitor"),
    ("hestia.gui.gtk_gui"),
)

imports = []
for module in builtins:
    loaded_module = __import__(module, globals(), locals(), [])
    for i in module.split(".")[1:]:
        loaded_module = getattr(loaded_module, i)
    imports.append(loaded_module)
        


class import_builtin(ImportBase):
    def load_imports(self):
        for i in imports:
            self.add_import(i)
