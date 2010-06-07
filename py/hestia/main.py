#from hestia.core.prompt import SimplePrompt
from circuits.core import Event, Component, Manager
from circuits import Debugger

import circuits.tools as tools
from hestia.core.plugins.loader_threaded import *

#from hestia.core.prompt import SimplePrompt
#from hestia.core.gnome_monitor import main as _main
from hestia.monitoring.statusicon import GtkStatusIcon
from hestia.monitoring.recompile  import Recompile
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
        m = Manager()
        m += Recompile(directory='py')
        m += GtkStatusIcon('py')
        #m += Debugger()
        #print tools.inspect(m)
        m.run()


    
def main():   
    main = Main()
    main.main()  
    return 0
    
if __name__ == "__main__":
    main()
