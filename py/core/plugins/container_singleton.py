from multiprocessing import Lock

class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, '_inst'):
            cls._inst_lock = Lock()
            cls._inst = super(Singleton, cls).__new__(cls)
        else:
            def init_pass(self, *dt, **mp):
                pass
            
            cls.__init__ = init_pass
            
        return cls._inst
    
