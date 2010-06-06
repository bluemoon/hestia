from pyinotify import *
from circuits import Debugger
from circuits.drivers._inotify import *
from circuits.core import Event, Component, Manager
from circuits import handler
from hestia import *

import logging
import subprocess

class E(Event): 
    def __init__(self, *args, **kwargs):
        super(E, self).__init__(*args, **kwargs)
        self.channel = self.__class__.__name__

class returncode(E):
    pass

class Recompile(Component):
    def __init__(self, command="make", directory='.'):
        super(Recompile, self).__init__(channel="inotify")

        self.command = command
        self.directory = directory 
        self.inotify = INotifyDriver(channel="inotify").register(self)
        self.inotify.add(directory, mask=IN_MODIFY)
        self.logger = logging.getLogger('')

        
    @handler("modified") 
    def on_modified(self, *args, **kwargs):  
        #print args, kwargs
        self.logger.debug("%s file modified" % args[2])
        self.logger.debug("Removing the watch on %s" % self.directory)
        self.inotify.remove(self.directory, recursive=True)
        self.logger.debug("Running %s" % self.command)
        #p = subprocess.Popen(self.command, shell=True)
        #subprocess.call(self.command, shell=True)
        proc = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = proc.wait()  
        print return_code
         
        self.inotify.add(self.directory, mask=IN_MODIFY)
        self.logger.debug("Adding the watch on %s" % self.directory)
        self.push(returncode(return_code)) 
         

