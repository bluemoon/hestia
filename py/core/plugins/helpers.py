from multiprocessing import Lock
from manager_default import DefaultPluginManager

class _Method:
    """Some magic to bind a method to a plugin.

    Supports "nested" methods (e.g. examples.getStateName).
    """
    def __init__(self, plugin, name):
        self.__plugin = plugin
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__plugin, "%s.%s" % (self.__name, name))

    def __call__(self, *args):
        return self.__plugin(self.__name, *args)

inst = None
inst_lock = Lock()

def instance():
    """Singleton constructor.
    """
    global inst
    global inst_lock
    inst_lock.acquire()
    try:
        if inst is None:
            inst = DefaultPluginManager()
            inst.loadPlugins()
        return inst
    finally:
        inst_lock.release()
