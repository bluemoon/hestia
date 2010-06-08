import subprocess
from circuits.core import Component

class cmd_runner(Component):        
    def cmd_run(self, command):
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = proc.wait()
        #print proc.communicate()
        print return_code
        return return_code
 
 
 
