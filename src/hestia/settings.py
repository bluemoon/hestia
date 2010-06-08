from hestia.structures.container_obj import ObjectProxy
from hestia.configobj.configobj import ConfigObj
import ConfigParser
import string
import os
import logging

defaults = {
    'global': {
        'debug' : False,
        },
    'project': {
        'monitor_directory' : '.',
        },
    

    }
class settingsException(Exception):
    pass

class settings:
    config = None
    def __init__(self):
        self.log = logging.getLogger('')
        config_files = ['.project.cfg', 'project.cfg', 'project.cfg.example']
        config_file = [x for x in config_files if os.path.exists(x)]
        if len(config_file) < 1:
            raise settingsException

        self.log.debug('using settings file "%s"' % config_file[0])
        config = ConfigObj(config_file[0], unrepr=True)
        self.settings = defaults
        self.settings.update(config)
        
        self.cp = ConfigParser.ConfigParser()
        self.cp.read(".project.cfg")
        self.config = ObjectProxy(self.settings)
        
    def __repr__(self):
        return repr(self.config)
        
 
