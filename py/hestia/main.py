from core.plugins.loader_threaded import *

import cmd
import sys
import time
import multiprocessing

class Simple(cmd.Cmd):
    def __init__(self, loader):
        cmd.Cmd.__init__(self)
        self.prompt = 'hestia% '
        self.loader = loader
        
    def do_greet(self, line):
        print "hello"
        
    def do_dict(self, line):
        self.loader.send_all('dict')
        if self.loader.poll_pipe('monitoring.monitor', 'basic_monitor'):
            print self.loader.receive('monitoring.monitor', 'basic_monitor')
        #print self.loader.get_queue('monitoring.monitor', 'basic_monitor')

    def do_msg(self, line):
        pieces = line.split(' ')
        self.loader.send(pieces[0], pieces[1], pieces[2])
        print self.loader.get_queue(pieces[0], pieces[1])
        
    def do_exit(self, line):
        self.loader.send_all('quit')
        sys.exit()
        
    def do_stats(self, line):
        print multiprocessing.active_children()
        #print multiprocessing._debug_info()
        
    def do_EOF(self, line):
        return True
    
class Main:
    def __init__(self):
        self.loader = loader_threaded()

        
    def main(self):
        Simple(self.loader).cmdloop()


def main():
    main = Main()
    main.main()
    
if __name__ == "__main__":
    main()
