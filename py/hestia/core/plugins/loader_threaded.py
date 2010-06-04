from multiprocessing import Process, Queue, Pipe, Lock
import multiprocessing
from loader import loader
from helpers import *
import inspect
import time
import sys
     
class loader_threaded(loader):
    def init(self, manager=None):
        #loader.__init__(self, manager)
        self.__Queues     = {}
        self.__Pipes      = {}
        self.__Processes  = {}
        self.__Lock       = {}
        
        
    def send_all(self, msg):
        for k, v in self.__Pipes.items():
            for k1, v1 in v.items():
                self.__Pipes[k][k1].send(msg)


    def poll_pipe(self, module_name, class_object):
        return self.__Pipes[module_name][class_object].poll()
    
    def send(self, module_name, class_object, msg):
        pass

    def receive(self, module_name, class_object):
        return self.__Pipes[module_name][class_object].recv()
    
    def get_queue(self, module_name, class_object):
        return self.__Queues[module_name][class_object].get()
    
    def __set_internal_data(self, module_name):
        if not hasattr(self.__Queues, module_name):
            self.__Queues[module_name] = {}
        if not hasattr(self.__Pipes, module_name):
            self.__Pipes[module_name] = {}
        if not hasattr(self.__Processes, module_name):
            self.__Processes[module_name] = {}
        if not hasattr(self.__Lock, module_name):
            self.__Lock[module_name] = {}
            
    def load_class(self, module, class_object):
        module_name = module.__name__
        parent, child = Pipe()
        #class_object.__bases__ = (threading_pattern,) + class_object.__bases__
        instance = class_object()
        parent_queue = Queue()
        lock = Lock()
        
        ##instance.setUp(child, parent_queue)
        self.__set_internal_data(module_name)
        
        self.__Queues[module_name][class_object.__name__] = parent_queue
        self.__Pipes[module_name][class_object.__name__]  = parent
        self.__Lock[module_name][class_object.__name__]  = lock
        
        self.class_instances[module.__name__][class_object.__name__] = instance
        process = Process(target=instance.run, args=(lock, child, parent_queue))
        self.__Processes[module_name][class_object.__name__] = process
        process.start()

        #parent.send(time.time())
        

