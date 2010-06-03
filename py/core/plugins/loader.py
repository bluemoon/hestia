from container_singleton import Singleton
from container_obj import ObjectProxy
from import_default import default_import_manager
from helpers import *

import helpers
import logging
import traceback
import inspect
import sys
import imp

import __builtin__
LOG_FILENAME = 'loader.log'
logging.raiseExceptions = False
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

class loader(Singleton):
    def __init__(self, manager=None):
        self.modules = {}
        self.module_classes = {}
        self.module_functions = {}
        self.class_instances = {}
        
        default = default_import_manager()
        default.load_imports()
        self.__imports = default.imports
        self.process_imports()

    def process_imports(self):
        for module in self.__imports:
            self.process_module(module)
            
    def __repr__(self):
        return ("<Loader for %s>" % (self.__imports))
    
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
        
    def load_class(self, class_object):
        return class_object()
    
    def system_loaded_module(self, module):
        if sys.modules.has_key(module):
            return sys.modules[module]
        else:
            return False
        
    def process_module(self, module):
        members = inspect.getmembers(module)
        self.module_classes[module] = {}
        self.module_functions[module] = {}
        self.class_instances[module] = {}
        
        for each in members:
            if inspect.isclass(each[1]):
                self.module_classes[module] = each
                self.class_instances[module][each[0]] = self.load_class(each[1])
            if inspect.isfunction(each[1]):
                self.module_functions[module] = each
                
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
    
        
