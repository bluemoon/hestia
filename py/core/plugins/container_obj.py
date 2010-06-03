import logging
from inspect import *
from helpers import *
import os
LOG_FILENAME = 'container_obj.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

class Obj(object):
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, (list, tuple)):
               setattr(self, key, [Obj(x) if isinstance(x, dict) else x for x in value])
            else:
               setattr(self, key, Obj(value) if isinstance(value, dict) else value)
               

class ObjectProxy(object):
    def __init__(self, constructor=None):
        self.__con = constructor
        self.__d = {}

    def __repr__(self):
        return '<ObjectProxy %s>' % repr(self.__d)
    
    def __getattr__(self, attr):
        #log(attr)
        #log(repr(self.__dict__))
        try:
            return dict.__getattr__(self, attr)
        except:
            if not self.__dict__.has_key(attr):
                self.__dict__[attr] = ObjectProxy()
            return self.__dict__[attr]
        
    def __setattr__(self, attr, value):
        #log(attr)
        #log(value)
        
        if self.__dict__.has_key(attr) or '__' in attr:
            dict.__setattr__(self, attr, value)
        else:
            self.__dict__[attr] =  value

