import time
import subprocess

from circuits import handler
from circuits.core import Event, Component
from circuits.drivers._inotify import *
from hestia.core.common_events import *
from hestia import *

MINUTE = 60
class git_monitor(Component):
    def __init__(self, freq=20*MINUTE, channel='git'):
        super(git_monitor, self).__init__(channel=channel)
        self._freq = freq
        self.target_time = time.time() + self._freq

    def __tick__(self):
        self.poll()
        
    def run(self):
        t = subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        
    def poll(self):
        if time.time() > self.target_time:
            self.run()
            rtime = time.time()
            self.target_time = rtime + self._freq
        


