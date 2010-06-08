import subprocess
from circuits.core import Component
from circuits import future

class cmd_runner(Component):
    #@future()
    def cmd_run(self, command):
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = proc.wait()
        return return_code#(return_code, comms)  
 
 
 
 
 
 
 
 
 
 
