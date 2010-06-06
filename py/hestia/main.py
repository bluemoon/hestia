from hestia.core.prompt import SimplePrompt
from hestia.core.plugins.loader_threaded import *
from recompile import Recompile

import logging as log

import cmd
import sys
import time
import threading
import sys


from . import fileHandler
fileHandler.doRollover()

class Main:  
    def main(self):
        self.event_driven = Recompile(directory='py')
        self.event_driven.start(process=True)
        self.loader = loader_threaded() 
        p = SimplePrompt(self.loader) 
        self.loader.process_imports() 
        threading.Thread(target=self.threaded).start()
         
    def threaded(self): 
        while True:
            for x in self.loader.process_iterator():
                x.is_alive() 
            if not self.loader.Queue.empty():
                msg = self.loader.Queue.get()
                log.debug("msg: " + msg) 
                if msg == "quit":
                    sys.exit()
   
def main():
    main = Main()
    main.main()
    return 0
    
if __name__ == "__main__":
    main()
