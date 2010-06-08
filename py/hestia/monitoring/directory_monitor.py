
import os
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
        self.directory = os.path.join(os.getcwd(), self.cfg.project.monitor_directory)
        self.build_cmd = self.cfg.build.command
        self.test_cmd  = self.cfg.test.command
        
        self.inotify = INotifyDriver().register(self)
        self.logger.debug("adding monitoring to %s" % self.directory)
        self.inotify.add(self.directory, mask=IN_MODIFY)

 
        
    def modified(self, *args, **kwargs):
        start = time.time()  
        #self.logger.debug("%s file modified" % args[2])
        self.logger.debug("removing directory '%s' from watchlist" % self.directory)
        self.inotify.remove(self.directory, recursive=True)
        
        self.logger.debug("Running build with %s" % self.build_cmd)
        build_return = self.push(cmd_run(self.build_cmd))
        self.logger.debug("Running tests with %s" % self.test_cmd)
        test_return  = self.push(cmd_run(self.test_cmd))
        self.inotify.add(self.directory, mask=IN_MODIFY)
        end = time.time()
        #if build_return == test_return:
        #print build_return
        self.push(returncode(end - start, self.build_cmd, (build_return, test_return)))
        #else: 
        #    print build_return, test_return
        #    self.push(returncode(1, end - start, self.test_cmd))

 
 
  
 
