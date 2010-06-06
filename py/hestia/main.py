from hestia.core.prompt import SimplePrompt
from hestia.core.plugins.loader_threaded import *
#from hestia.core.event_driven import *

import logging as log

import cmd
import sys
import time
import multiprocessing
import threading
import sys

from hestia.circuits import *
from hestia.circuits.drivers._inotify import INotifyDriver

from . import fileHandler
fileHandler.doRollover()

class EventDriven:
    def test(self):
        driver = INotifyDriver()
        driver.add('py')
        driver.run()
        print driver
        
class Main:
    def main(self):
        self.event_driven = EventDriven()
        self.event_driven.test()
        
        self.loader = loader_threaded()
        p = SimplePrompt(self.loader)
        self.loader.process_imports()
        #threading.Thr ead(target=p.cmdloop).start()
        threading.Thread(target=self.threaded).start()
        #p.cmdloop()
        
    def threaded(self):
        #iteration = 0
        while True:
            for x in self.loader.process_iterator():
                x.is_alive()
                
            if not self.loader.Queue.empty():
                msg = self.loader.Queue.get()
                log.debug("msg: " + msg)
                if msg == "quit":
                    sys.exit()
   
            #iteration += 1
def main():
    main = Main()
    main.main()
    return 0
    
if __name__ == "__main__":
    main()
