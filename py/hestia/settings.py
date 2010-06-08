from hestia.core.structures.container_obj import ObjectProxy
from hestia.configobj.configobj import ConfigObj
import ConfigParser
import string

class settings:
    config = None
    def __init__(self):
        self.settings = ConfigObj('.project.cfg', unrepr=True)
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(".project.cfg")
        self.config = ObjectProxy(self.settings)
        
    def __repr__(self):
        return repr(self.config)
        
 
