from multiprocessing import Lock
from import_default import DefaultPluginManager

import inspect
import traceback
import logging

def current():
    return inspect.stack()[1][3]

def parent():
    return inspect.stack()[2][3]

def log(data):
    Stack = inspect.stack()[1]
    logging.debug("%d %s: %s" % (Stack[2], os.path.split(Stack[1])[1], data))
 
def log_traceback():
    logging.debug(repr(traceback.format_exc()))
    
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
