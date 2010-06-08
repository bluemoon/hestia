#from hestia.core.prompt import SimplePrompt
import imp
import inspect as inspector
from circuits.core import Manager, Debugger, Component
from circuits.tools import inspect
from hestia.settings import settings

from hestia.monitoring.directory_monitor import directory_monitor
from hestia.ui.statusicon import gtk_status_icon
from hestia.ui.notifications import notifications
from hestia.core.cmd_runner import cmd_runner
from hestia.__version__ import version

from . import fileHandler
fileHandler.doRollover()

from hestia.core.plugins.import_default import default_import_manager
class basic_loader:
    def __init__(self):
        default = default_import_manager()
        default.load_imports()
        self.__imports = default.imports
        print self.__imports

    def process_modules(self):
        for imported in self.__imports:
            self.process_classes(imported)
            
    def process_classes(self, imported):
        for key, value in imported.__dict__.items():
            if inspector.isclass(value):
                if issubclass(value, Component):
                    #print value
                    pass
                        
            #if issubclass(cls, base):
            #    for k, v in base.__dict__.items():
            #        p1 = callable(v)
class Main:
    def startup(self):
        print 'starting Hestia v%s' % version
        self.loader = basic_loader()
        self.loader.process_modules()
        
    def main(self):
        self.startup() 
        s = settings()
        m = Manager()
        m += directory_monitor(s) 
        m += cmd_runner(s)  
        m += gtk_status_icon(s)
        m += notifications()  

        # m += Debugger() 
        #print inspect(m) 
        m.run()
 
 
     
def main():   
    main = Main()
    main.main()  
    return 0 
    
if __name__ == "__main__":
    main()
