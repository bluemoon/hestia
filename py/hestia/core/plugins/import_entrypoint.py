#from manager_base import PluginManager
from import_base import ImportBase
try:
    from pkg_resources import iter_entry_points
    has_pkg = True
except ImportError:
    has_pkg = False

class import_entrypoint(ImportBase):
    def load_imports(self):
        if not has_pkg:
            return

        for entrypoint in ['hestia']:
            for ep in iter_entry_points(entrypoint):
                try:
                    plug = ep.load()
                except Exception, e:
                    warn("Unable to load plugin %s: %s" % (ep, e), RuntimeWarning)
                    continue
                #self._loadPlugin(plug())
                #print plug

