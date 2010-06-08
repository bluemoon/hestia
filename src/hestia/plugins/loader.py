from hestia.structures.singleton import *
from hestia.structures.container_obj import ObjectProxy
from import_default import default_import_manager

from helpers import *
from multiprocessing import *

import helpers
import threading
import logging as log
import traceback
import inspect
import sys
import imp


class loader(Singleton3):
    def __init__(self, manager=None):
        self.modules            = {}
        self.module_classes     = {}
        self.module_functions   = {}
        self.class_instances    = {}
        self.proxy_objects      = {}

        default = default_import_manager()
        default.load_imports()
        self.__imports = default.imports
        log.debug("processing imports")
        #log.debug("stuff and things")

    def process_imports(self):
        for module in self.__imports:
            #log.debug(module)
            #t = threading.Thread(target=self.process_module, args=(module,))
            #t.start()
            self.process_module(module)
            
            
    def __repr__(self):
        return ("<Loader for %s>" % (self.__imports))

    def get_instance(self, name):
        proxy_object = ObjectProxy()
        if self.class_instances.has_key(name):
            for k, v in self.class_instances[name].items():
                setattr(proxy_object, k, v)
        else:
            return
            
        return proxy_object
    
    @property
    def get_modules(self):
        return self.modules

    @property
    def get_classes(self):
        return self.module_classes
    
    @property
    def get_class_instances(self):
        return self.class_instances

    @property
    def get_function(self):
        return self.module_functions
    

    def get_module(self, module):
        if self.modules.has_key(module):
            return self.modules[module]
        else:
            return False
        
    #def __getattr__(self, attr):
    #    if attr in self.__dict__:
    #        return self.__dict__[attr] 
    #    elif attr in self.class_instances:
    #        return self.class_instances[attr]
            
    def load_class(self, module, class_object):
        pass
        #self.class_instances[module.__name__][class_object.__name__] = class_object()

    def system_loaded_module(self, module):
        if sys.modules.has_key(module):
            return sys.modules[module]
        else:
            return False
        
    
    def process_module(self, module):
        members = inspect.getmembers(module)
        module_name = module.__name__
        self.module_classes[module_name] = {}
        self.module_functions[module_name] = {}
        self.class_instances[module_name] = {}
        
        for each in members:
            if inspect.isclass(each[1]):
                self.module_classes[module_name] = each
                self.load_class(module, each[1])
            if inspect.isfunction(each[1]):
                self.module_functions[module_name] = each
                
    def load_module(self, module, location=None):
        local_module = self.get_module(module)
        system_module = self.system_loaded_module(module)
        if not local_module and not system_module:
            try:
                file, pathname, description = imp.find_module(module)
                loaded_module = imp.load_module(name, file, pathname, description)
                file.close()
                
            except Exception, E:
                try:
                    loaded_module = __import__(module, globals(), locals(), [], -1)
                except Exception, E2:
                    raise ImportError

            self.modules[module] = loaded_module
            
        self.process_module(self.modules[module])

        #print self.module_classes
        #print self.module_functions
        #print self.class_instances
    
        
