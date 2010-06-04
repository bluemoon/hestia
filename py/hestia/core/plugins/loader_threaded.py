from multiprocessing import Process, Queue, Pipe, Lock
from hestia.core.plugins.scheduler import *
import multiprocessing
from loader import loader
from helpers import *
import inspect
import time
import sys

def handle(message):
    print "[%s] MESSAGE: %s" % (time.time(), message) 

class loader_threaded(loader):
    def init(self, manager=None):
        self.__Queues     = {}
        self.__Pipes      = {}
        self.__Processes  = {}
        self.__Lock       = {}
        
        self.sched_queue   = Queue()
        self.sched         = Scheduler(self.sched_queue, handle) 
        self.sched_process = Process(target=self.sched.run, args=())
        self.sched_process.start()
        
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
        parent_queue = Queue()
        lock = Lock()
        print class_object
        instance = class_object(child=child, parent=parent_queue)
        self.__set_internal_data(module_name)
        
        self.__Queues[module_name][class_object.__name__] = parent_queue
        self.__Pipes[module_name][class_object.__name__]  = parent
        self.__Lock[module_name][class_object.__name__]  = lock
        
        self.class_instances[module.__name__][class_object.__name__] = instance
        process = Process(target=instance.run, args=(lock, child, parent_queue))
        self.__Processes[module_name][class_object.__name__] = process
        process.start()
        

