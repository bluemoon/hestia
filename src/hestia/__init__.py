import logging 
import logging.handlers
import sys

TERM_GREEN   = "\033[1;32m"
TERM_ORANGE  = '\033[93m'
TERM_BLUE    = '\033[94m'
TERM_RED     = '\033[91m'
TERM_END     = "\033[1;m"
DATE_FMT     = '%H:%M:%S'
FORMAT = '%(asctime)s %(levelname)s: [m:%(module)s f:%(funcName)s  l:%(lineno)s]: %(message)s' 
LOG_FILENAME = 'logs/hestia.log'

fileHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME)

logging.raiseExceptions = False
formatter = logging.Formatter(FORMAT, datefmt=DATE_FMT)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
fileHandler.setFormatter(formatter)
logger=logging.getLogger('')
logger.addHandler(stdout_handler)
logger.addHandler(fileHandler) 
logger.setLevel(logging.DEBUG)
##> > logging.debug('A debug message')
##> > logging.info('Some information')
##> > logging.warning('A shot across the bows')


