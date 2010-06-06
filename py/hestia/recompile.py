from pyinotify import *
from circuits import Debugger
from circuits.drivers._inotify import *
from circuits.core import Event, Component
from circuits import handler

class Command(Event):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.channel = self.__class__.__name__


class Recompile(Component):
    def __init__(self, freq=1, timeout=1, command="make", directory=None):
        super(Recompile, self).__init__(channel="inotify")
        #self += Debugger() 
        #self += INotifyDriver() + Debugger()
        self._freq = freq
        self.command = command
        self.directory = directory
        self.inotify = INotifyDriver().register(self)
        self.inotify.add(directory, mask=IN_MODIFY)
        self.logger = logging.getLogger('')
        
    @handler("modified") 
    def on_modified(self, *args, **kwargs):  
        #print args, kwargs
        self.logger.debug("%s file modified" % args[2])
        self.logger.debug("Removing the watch on %s" % self.directory)
        self.inotify.remove(self.directory, recursive=True)
        self.logger.debug("Running %s" % self.command)
        p = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()  
        self.inotify.add(self.directory, mask=IN_MODIFY)
        self.logger.debug("Adding the watch on %s" % self.directory)
        
