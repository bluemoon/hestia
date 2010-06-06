from multiprocessing import Process, Queue, Pipe, Lock
from threading import Thread
from hestia.core.plugins.scheduler import *
import multiprocessing
from loader import loader
from helpers import *
import logging as log
import inspect
import time
import sys

class dispatch(Thread):
    def __init__(self, lock, child, parent_queue, class_obj):
        super(dispatch, self).__init__()
        self.lock = lock
        self.child = child
        self.parent_queue = parent_queue
        self.class_object = class_obj

    def run(self):
        instance = self.class_object(child=self.child, parent=self.parent_queue)
        instance.run(self.lock, self.child, self.parent_queue)
        
class loader_threaded(loader):
    def init(self, manager=None):
        self.__Queues     = {}
        self.__Pipes      = {}
        self.__Processes  = {}
        self.__Lock       = {}
        
        self.sched        = scheduler([self.check_for_quit]) 
        self.sched.start()
        
    def send_all(self, msg):
        for key, value in self.__Pipes.items():
            for subkey, subvalue in value.items():
                self.__Pipes[key][subkey].send(msg)

    def get_all(self):
        for k, v in self.__Queues.items():
            for k1, v1 in v.items():
                yield self.__Queues[k][k1].get()
                
    def check_for_quit(self):
        for x in self.get_all():
            if x == 'quit':
                sys.exit()
            
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
        class_name  = class_object.__name__
        
        parent, child = Pipe()
        parent_queue = Queue()
        lock = Lock()

        self.__set_internal_data(module_name)
        self.__Queues[module_name][class_name] = parent_queue
        self.__Pipes[module_name][class_name]  = parent
        self.__Lock[module_name][class_name]  = lock
        log.debug("dispatching a new thread for class %s in %s module" % (class_name, module_name))
        process = dispatch(lock, child, parent_queue, class_object).start()
        #instance = class_object(child=child, parent=parent_queue)
        
        #self.class_instances[module.__name__][class_object.__name__] = instance
        #thread = threading.Thread(target=instance.run)        
        #process = Process(target=instance.run, args=(lock, child, parent_queue))
        self.__Processes[module_name][class_object.__name__] = process
        #process.start()
        

