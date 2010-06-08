#from hestia.core.prompt import SimplePrompt
from circuits.core import Manager
from hestia.monitoring.directory_monitor import directory_monitor
from hestia.monitoring.statusicon import gtk_status_icon

from . import fileHandler


fileHandler.doRollover()

class Main:  
    def main(self):
        m = Manager()
        m += directory_monitor(directory='py')
        m += gtk_status_icon('py')
        #m += Debugger()
        #print tools.inspect(m)
        m.run()


    
def main():   
    main = Main()
    main.main()  
    return 0
    
if __name__ == "__main__":
    main()
