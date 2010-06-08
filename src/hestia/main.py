from optparse import OptionParser
from circuits import Debugger
from circuits.tools import inspect
from circuits.core import Manager
from hestia.__version__ import version
from hestia.settings import settings
from hestia.core.cmd_runner import cmd_runner
from hestia.monitoring import *
from hestia.ui import *
import logging as log

from . import fileHandler
fileHandler.doRollover()

class Main:
    def __init__(self, options):
        self.options = options
        if not self.options.verbose:
            self.log = log.getLogger('')
            self.log.setLevel(log.ERROR)
        
    def startup(self):
        print 'starting Hestia v%s' % version
        
    def main(self):
        self.startup()
        config = settings.settings()
        m = Manager()
        m += directory_monitor(config)
        m += git_monitor()
        m += cmd_runner(config)  
        m += gtk_status_icon(config)
        m += notifications()
        
        if self.options.verbose:
            m += Debugger()
            print inspect(m)
            
        m.run()
 
 
     
def main():
    parser = OptionParser()
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)
    (options, args) = parser.parse_args()
    
    main = Main(options)
    main.main()  
    return 0 
    
if __name__ == "__main__":
    main()
