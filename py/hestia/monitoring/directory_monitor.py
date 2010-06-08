import subprocess

from circuits import handler
from circuits.core import Event, Component
from circuits.drivers._inotify import *
from hestia.core.common_events import *
from hestia import *

from pyinotify import *

class directory_monitor(Component):
    def __init__(self, settings):
        self.logger = logging.getLogger('')
        super(directory_monitor, self).__init__(channel="inotify")
        self.cfg = settings.config
        self.directory = self.cfg.project.monitor_directory
        self.build_cmd = self.cfg.build.command
        self.test_cmd  = self.cfg.test.command
        
        self.inotify = INotifyDriver(channel="inotify").register(self)
        self.logger.debug("adding monitoring to %s" % self.directory)
        self.inotify.add(self.directory, mask=IN_MODIFY)
 

        
    def modified(self, *args, **kwargs):
        start = time.time() 
        self.logger.debug("%s file modified" % args[2])
        self.inotify.remove(self.directory, recursive=True)
        self.logger.debug("Running build with %s" % self.build_cmd)
        
        build_return = self.push(cmd_run(self.build_cmd))
        end = time.time()
        self.push(returncode(build_return, end - start, self.build_cmd))

        start = time.time()

        test_return  = self.push(cmd_run(self.test_cmd))
        self.logger.debug("Running tests with %s" % self.test_cmd)
        self.inotify.add(self.directory, mask=IN_MODIFY)
        end = time.time()
        self.push(returncode(build_return, end - start, self.test_cmd))

 
 
