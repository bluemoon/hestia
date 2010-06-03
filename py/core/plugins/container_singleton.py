from multiprocessing import Lock
from helpers import *
import inspect
import __builtin__
__builtin__.instance = {}

def init_pass(self, *dt, **mp):
    pass

class Singleton(object):
    def __new__(cls):
        mro = inspect.getmro(cls)[:-2]
        ## if we dont have `_inst`, make it
        if not hasattr(cls, '_inst'):
            cls._inst_lock = Lock()
            cls._inst = super(Singleton, cls).__new__(cls)
        else:

            
            cls.__init__ = init_pass
            
        return cls._inst

class Singleton2(object):
    __instance = None
    def __new__(typ, *args, **kwargs):
        if Singleton2.__instance == None:
            obj = object.__new__(typ, *args, **kwargs)
            Singleton2.__instance = obj
            
        return Singleton2.__instance
 
