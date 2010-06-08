import time
import subprocess

from circuits import handler
from circuits.core import Event, Component
from circuits.drivers._inotify import *
from hestia.core.common_events import *
from hestia import *

MINUTE = 60

class git_monitor(Component):
    def __init__(self, freq=20, channel='git'):
        super(git_monitor, self).__init__(channel=channel)
        self._freq = freq

    def _sleep(self, rtime):
        if self._freq > 0:
            ctime = time.time()
            s = self._freq - (ctime - rtime)
            if s > 0:
                time.sleep(s)
                
        
    def __tick__(self):
        print 'tick'
        t = subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        rtime = time.time()
        self._sleep(rtime)

