#from multiprocessing import Process, Queue, Pipe, Lock
from hestia.core.plugins.scheduler import *
from threading import Thread, current_thread
from multiprocessing import Pipe, Lock
from loader import loader
from helpers import *
from Queue import Queue
import logging as log
import inspect
import time
import sys


class dispatch(Thread):
    def __init__(self, lock, child, parent_queue, class_obj):
        Thread.__init__(self)
        log.debug(child)
        
        self.lock = lock
        self.child = child
        self.parent_queue = parent_queue
        self.class_object = class_obj

    def run(self):
        instance = self.class_object(self.child, self.parent_queue, self.lock)
        log.debug(current_thread())
        instance.run()
        log.debug("leaving run")
        
        
class loader_threaded(loader):
    def __init__(self, manager=None):
        self.Queues     = {}
        self.Pipes      = {}
        self.Processes  = {}
        self.Lock       = {}
        self.Queue      = Queue()
        loader.__init__(self, manager)
        #log.debug(self.__dict__)        
        #self.sched        = scheduler([self.check_for_quit]) 
        #self.sched.start()
        
    def send_all(self, msg):
        for key, value in self.Pipes.items():
            for subkey, subvalue in value.items():
                self.Pipes[key][subkey].send(msg)

    def get_all(self):
        for key, value in self.Queues.items():
            for subkey, subvalue in value.items():
                if not self.Queues[key][subkey].empty():
                    yield (self.Queues[key][subkey].get())
                
    def check_for_quit(self):
        for x in self.get_all():
            if x == 'quit':
                sys.exit()
            
    def poll_pipe(self, module_name, class_object):
        return self.Pipes[module_name][class_object].poll()
    
    def send(self, module_name, class_object, msg):
        pass

    def receive(self, module_name, class_object):
        return self.Pipes[module_name][class_object].recv()
    
    def get_queue(self, module_name, class_object):
        return self.Queues[module_name][class_object].get()
    
    def process_iterator(self):
        for key, value in self.Processes.items():
            for subkey, subvalue in value.items():
                yield self.Processes[key][subkey]
                
    def __set_internal_data(self, module_name):
        if not hasattr(self.Queues, module_name):
            self.Queues[module_name] = {}
        if not hasattr(self.Pipes, module_name):
            self.Pipes[module_name] = {}
        if not hasattr(self.Processes, module_name):
            self.Processes[module_name] = {}
        if not hasattr(self.Lock, module_name):
            self.Lock[module_name] = {}
                
    def load_class(self, module, class_object):
        module_name = module.__name__
        class_name  = class_object.__name__
        
        parent, child = Pipe()
        parent_queue = Queue()
        lock = Lock()

        self.__set_internal_data(module_name)
        self.Queues[module_name][class_name] = parent_queue
        self.Pipes[module_name][class_name]  = parent
        self.Lock[module_name][class_name]   = lock
        log.debug("dispatching a new thread for class %s in %s module" % (class_name, module_name))
        process = dispatch(lock, child, self.Queue, class_object)
        process.start()
        #process.join()
        #instance = class_object(child=child, parent=parent_queue)
        log.debug("does this block?")
        self.class_instances[module.__name__][class_object.__name__] = instance
        #thread = threading.Thread(target=instance.run)        
        #process = Process(target=instance.run, args=(lock, child, parent_queue))
        #self.__Processes[module_name][class_object.__name__] = process
        #process.start()
        

