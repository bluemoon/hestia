import inspect
import traceback
import logging

def current():
    return inspect.stack()[1][3]

def parent():
    return inspect.stack()[2][3]

def log(data):
    Stack = inspect.stack()[1]
    logging.debug("%d %s: %s" % (Stack[2], os.path.split(Stack[1])[1], data))
 
def log_traceback():
    logging.debug(repr(traceback.format_exc()))
