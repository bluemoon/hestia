from import_base  import ImportBase
from helpers      import locate
from os           import path

import os
import sys
import imp

import logging as log

class import_directory(ImportBase):
    def init(self, *args, **kwargs):
        self.__default_directory = path.join(path.dirname(imp.find_module("hestia")[1]), "hestia")  
        self.__directories = [self.__default_directory]
        self.__blacklist = ['core','plugins', 'tests']
        
    def load_imports(self):
        imports = []
        for directory in self.__directories:
            for subdirectory in os.listdir(directory):
                subdirectory = path.join(directory, subdirectory)
                if subdirectory in self.__blacklist:
                    continue
                
                for py in locate("*.py", root=subdirectory):
                    print py
                    tail, head = path.split(py)
                    name = path.splitext(head)
                    if name != "__init__":
                        log.debug((name[0], tail))
                        imports.append((name[0], tail))
            
        fh = None
        for (name, dir_) in imports:
            print name, dir_
            fh, filename, desc = imp.find_module(name, [dir_])
            log.debug((fh, filename, desc))
            if sys.modules.has_key(name):
                old = sys.modules[name]
                if old is not None:
                    del sys.modules[name]

            try:
                mod = imp.load_module(name, fh, filename, desc)
            except:
                continue
            self.add_import(mod)
            
            if fh:
                fh.close()
                
