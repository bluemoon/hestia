import inspect
import traceback
import logging
import os
import fnmatch

def current():
    return inspect.stack()[1][3]

def parent():
    return inspect.stack()[2][3]

def log(data):
    Stack = inspect.stack()[1]
    logging.debug("%d %s: %s" % (Stack[2], os.path.split(Stack[1])[1], data))
 
def log_traceback():
    logging.debug(repr(traceback.format_exc()))
    
def itersubclasses(cls, _seen=None):
    """
    itersubclasses(cls)

    Generator over all subclasses of a given class, in depth first order.

    >>> list(itersubclasses(int)) == [bool]
    True
    >>> class A(object): pass
    >>> class B(A): pass
    >>> class C(A): pass
    >>> class D(B,C): pass
    >>> class E(D): pass
    >>> 
    >>> for cls in itersubclasses(A):
    ...     print(cls.__name__)
    B
    D
    E
    C
    >>> # get ALL (new-style) classes currently defined
    >>> [cls.__name__ for cls in itersubclasses(object)] #doctest: +ELLIPSIS
    ['type', ...'tuple', ...]
    """
    
    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with '
                        'new-style classes, not %.100r' % cls)
    if _seen is None:
        _seen = set()
    try:
        subs = cls.__subclasses__()
    except TypeError: # fails only when cls is type
        subs = cls.__subclasses__(cls)
    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for sub in itersubclasses(sub, _seen):
                yield sub
                
def get_super_classes(cls):
    return [o[0] for o in inspect.getclasstree([cls]) if type(o[0]) == type]

class _Method:
    """Some magic to bind a method to a plugin.

    Supports "nested" methods (e.g. examples.getStateName).
    """
    def __init__(self, plugin, name):
        self.__plugin = plugin
        self.__name = name

    def __getattr__(self, name):
        return _Method(self.__plugin, "%s.%s" % (self.__name, name))

    def __call__(self, *args):
        return self.__plugin(self.__name, *args)
    
def locate(pattern, root=os.getcwd()):
    for path, dirs, files in os.walk(root):
        for filename in [os.path.abspath(os.path.join(path, filename)) for filename in files if fnmatch.fnmatch(filename, pattern)]:
            yield filename
            
def difference(a, b):
    """ show whats in list b which isn't in list a """
    return list(set(b).difference(set(a)))
