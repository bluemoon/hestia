#from hestia.core.prompt import SimplePrompt
from circuits.core import Event, Component, Manager
from circuits import Debugger
from hestia.core.plugins.loader_threaded import *
from hestia.core.recompile import Recompile
from hestia.core.prompt import SimplePrompt
from hestia.core.gnome_monitor import main as _main
from hestia.monitoring.gnome_notification import GtkStatusIcon

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
        #manager = Manager()
        #manager += Recompile()
        #manager += INotifyDriver()
        m = Manager()
        m += Recompile(directory='py')
        m += GtkStatusIcon('py')
        m += Debugger()

        m.start(process=True) 

        #self.event_driven = Recompile(directory='py') + 
        #self.event_driven.start(process=True)
        
        #self.status_icon = 
        #self.status_icon.start(process=True)
        #self.loader = loader_threaded() 
        #self.loader.process_imports()
        #_main(sys.argv)
  
        
        p = SimplePrompt()
        p.cmdloop()
        #threading.Thread(target=self.threaded).start()
         
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
