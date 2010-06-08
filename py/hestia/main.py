#from hestia.core.prompt import SimplePrompt
from circuits.core import Manager, Debugger
from circuits.tools import inspect
from hestia.settings import settings

from hestia.monitoring.directory_monitor import directory_monitor
from hestia.ui.statusicon import gtk_status_icon
from hestia.ui.notifications import notifications
from hestia.core.cmd_runner import cmd_runner
from hestia.__version__ import version

from . import fileHandler
fileHandler.doRollover()

class Main:
    def startup(self):
        print 'starting Hestia v%s' % version
        
    def main(self):
        self.startup() 
        s = settings()
        m = Manager()
        m += directory_monitor(s) 
        m += cmd_runner(s)  
        m += gtk_status_icon(s)
        m += notifications()  

        # m += Debugger() 
        print inspect(m) 
        m.run()
 

     
def main():   
    main = Main()
    main.main()  
    return 0 
    
if __name__ == "__main__":
    main()
