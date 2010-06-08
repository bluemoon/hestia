import os
import new
import time
import signal

from signal import *
from threading import Thread
from collections import deque
from operator import attrgetter
from sys import exc_info as _exc_info
from sys import exc_clear as _exc_clear
from inspect import getargspec, getmembers

from itertools import chain
from multiprocessing import Process
from multiprocessing import current_process as process
from multiprocessing import active_children as processes
from pyinotify import IN_UNMOUNT
from pyinotify import WatchManager, Notifier, ALL_EVENTS
from pyinotify import IN_ACCESS, IN_MODIFY, IN_ATTRIB, IN_CLOSE_WRITE
from pyinotify import IN_CREATE, IN_DELETE, IN_DELETE_SELF, IN_MOVE_SELF
from pyinotify import IN_CLOSE_NOWRITE, IN_OPEN, IN_MOVED_FROM, IN_MOVED_TO

HAS_MULTIPROCESSING = 1
    
class Event(object):
    channel = None
    target = None

    def __init__(self, *args, **kwargs):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"
        self.args = args
        self.kwargs = kwargs

    @property
    def name(self):
        return self.__class__.__name__

    def __eq__(self, other):
        """ x.__eq__(other) <==> x==other

        Tests the equality of Event self against Event y.
        Two Events are considered "equal" iif the name,
        channel and target are identical as well as their
        args and kwargs passed.
        """

        return (self.__class__ is other.__class__
                and self.channel == other.channel
                and self.args == other.args
                and self.kwargs == other.kwargs)

    def __repr__(self):
        "x.__repr__() <==> repr(x)"

        if type(self.channel) is tuple:
            channel = "%s:%s" % self.channel
        else:
            channel = self.channel or ""
        return "<%s[%s] %s %s>" % (self.name, channel, self.args, self.kwargs)

    def __getitem__(self, x):
        """x.__getitem__(y) <==> x[y]

        Get and return data from the Event object requested by "x".
        If an int is passed to x, the requested argument from self.args
        is returned index by x. If a str is passed to x, the requested
        keyword argument from self.kwargs is returned keyed by x.
        Otherwise a TypeError is raised as nothing else is valid.
        """

        if type(x) is int:
            return self.args[x]
        elif type(x) is str:
            return self.kwargs[x]
        else:
            raise TypeError("Expected int or str, got %r" % type(x))

class Error(Event):
    channel = "exception"

    def __init__(self, type, value, traceback, **kwargs):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"

        super(Error, self).__init__(type, value, traceback, **kwargs)


class Started(Event):
    """Started Event

    This Event is sent when a Component has started running.

    @param component: The component that was started
    @type  component: Component or Manager

    @param mode: The mode in which the Component was started,
                 P (Process), T (Thread) or None (Main Thread / Main Process).
    @type  str:  str or None
    """

    def __init__(self, component, mode):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"
        super(Started, self).__init__(component, mode)


class Stopped(Event):
    """Stopped Event

    This Event is sent when a Component has stopped running.

    @param component: The component that has stopped
    @type  component: Component or Manager
    """

    def __init__(self, component):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"

        super(Stopped, self).__init__(component)

class Signal(Event):
    """Signal Event

    This Event is sent when a Component receives a signal.

    @param signal: The signal number received.
    @type  int:    An int value for the signal

    @param stack:  The interrupted stack frame.
    @type  object: A stack frame
    """

    def __init__(self, signal, stack):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"

        super(Signal, self).__init__(signal, stack)


class Registered(Event):
    """Registered Event

    This Event is sent when a Component has registered with another Component
    or Manager. This Event is only sent iif the Component or Manager being
    registered with is not itself.

    @param component: The Component being registered
    @type  component: Component

    @param manager: The Component or Manager being registered with
    @type  manager: Component or Manager
    """

    def __init__(self, component, manager):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"

        super(Registered, self).__init__(component, manager)

class Unregistered(Event):
    """Unregistered Event

    This Event is sent when a Component has been unregistered from it's
    Component or Manager.
    """

    def __init__(self, component, manager):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"

        super(Unregistered, self).__init__(component, manager)

_sortkey = attrgetter("priority", "filter")

def handler(*channels, **kwargs):
    """Creates an Event Handler

    Decorator to wrap a callable into an Event Handler that
    listens on a set of channels defined by channels. The type
    of the Event Handler defaults to "listener". If kwargs["filter"]
    is defined and is True, the Event Handler is defined as a
    Filter and has priority over Listener Event Handlers.
    If kwargs["target"] is defined and is not None, the
    Event Handler will listen for the spcified channels on the
    spcified Target Component's Channel.
    
    Examples:
       >>> @handler("foo")
       ... def foo():
       ...     pass
       >>> @handler("bar", filter=True)
       ... def bar():
       ...     pass
       >>> @handler("foo", "bar")
       ... def foobar():
       ...     pass
       >>> @handler("x", target="other")
       ... def x():
       ...     pass
    """

    def wrapper(f):
        if channels and type(channels[0]) is bool and not channels[0]:
            f.handler = False
            return f

        f.handler = True

        f.override = kwargs.get("override", False)
        f.priority = kwargs.get("priority", 0)

        f.filter = kwargs.get("filter", False)

        f.target = kwargs.get("target", None)
        f.channels = channels

        f.args, f.varargs, f.varkw, f.defaults = getargspec(f)
        if f.args and f.args[0] == "self":
            del f.args[0]
        if f.args and f.args[0] == "event":
            f._passEvent = True
        else:
            f._passEvent = False

        return f

    return wrapper

class HandlersType(type):
    """Handlers metaclass

    metaclass used by the Component to pick up any methods defined in the new
    Component and turn them into Event Handlers by applying the @handlers
    decorator on them. This is done for all methods defined in the Component
    that:
     - Do not start with a single '_'. or
     - Have previously been decorated with the @handlers decorator
    """

    def __init__(cls, name, bases, dct):
        "x.__init__(...) initializes x; see x.__class__.__doc__ for signature"

        super(HandlersType, cls).__init__(name, bases, dct)

        for k, v in dct.iteritems():
            if callable(v) and not (k[0] == "_" or hasattr(v, "handler")):
                setattr(cls, k, handler(k)(v))

class Manager(object):
    """Manager

    This is the base Manager of the BaseComponent which manages an Event Queue,
    a set of Event Handlers, Channels, Tick Functions, Registered and Hidden
    Components, a Task and the Running State.

    @ivar manager: The Manager of this Component or Manager
    """

    def __init__(self, *args, **kwargs):
        "initializes x; see x.__class__.__doc__ for signature"

        self._queue = deque()
        self._handlers = set()
        self._globals = []
        self.channels = dict()
        self._cmap = dict()
        self._tmap = dict()

        self._ticks = set()
        self.components = set()

        self._task = None
        self._running = False

        self.root = self
        self.manager = self

    def __repr__(self):
        "x.__repr__() <==> repr(x)"

        name = self.__class__.__name__
        q = len(self._queue)
        c = len(self.channels)
        h = len(self._handlers)
        state = self.state
        format = "<%s (q: %d c: %d h: %d) [%s]>"
        return format % (name, q, c, h, state)

    def __len__(self):
        """x.__len__() <==> len(x)

        Returns the number of events in the Event Queue.
        """

        return len(self._queue)

    def __add__(self, y):
        """x.__add__(y) <==> x+y

        (Optional) Convenience operator to register y with x
        Equivalent to: y.register(x)

        @return: x
        @rtype Component or Manager
        """

        y.register(self)
        return self
    
    def __iadd__(self, y):
        """x.__iadd__(y) <==> x += y

        (Optional) Convenience operator to register y with x
        Equivalent to: y.register(x)

        @return: x
        @rtype Component or Manager
        """

        y.register(self)
        return self

    def __sub__(self, y):
        """x.__sub__(y) <==> x-y

        (Optional) Convenience operator to unregister y from x.manager
        Equivalent to: y.unregister()

        @return: x
        @rtype Component or Manager
        """

        if y.manager == self:
            y.unregister()
            return self
        else:
            raise TypeError("No registration found for %r" % y)

    def __isub__(self, y):
        """x.__sub__(y) <==> x -= y

        (Optional) Convenience operator to unregister y from x
        Equivalent to: y.unregister()

        @return: x
        @rtype Component or Manager
        """

        if y.manager == self:
            y.unregister()
            return self
        else:
            raise TypeError("No registration found for %r" % y)

    def _getHandlers(self, _channel):
        target, channel = _channel

        channels = self.channels
        exists = self.channels.has_key
        get = self.channels.get
        tmap = self._tmap.get
        cmap = self._cmap.get

        # Global Channels
        handlers = self._globals
  
        # This channel on all targets
        if channel == "*":
            all = tmap(target, [])
            return chain(handlers, all)

        # Every channel on this target
        if target == "*":
            all = cmap(channel, [])
            return chain(handlers, all)

        # Any global channels
        if exists(("*", channel)):
            handlers = chain(handlers, get(("*", channel)))
 
        # Any global channels for this target
        if exists((channel, "*")):
            handlers = chain(handlers, get((channel, "*")))

        # The actual channel and target
        if exists(_channel):
            handlers = chain(handlers, get((_channel)))
  
        return handlers

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def running(self):
        return self._running

    @property
    def state(self):
        if self.running:
            if self._task is None:
                return "R"
            else:
                if self._task.isAlive():
                    return "R"
                else:
                    return "D"
        else:
            return "S"

    def _add(self, handler, channel=None):
        """E._add(handler, channel) -> None

        Add a new Event Handler to the Event Manager
        adding it to the given channel. If no channel is
        given, add it to the global channel.
        """

        if channel is None:
            if handler not in self._globals:
                self._globals.append(handler)
                self._globals.sort(key=_sortkey)
                self._globals.reverse()
        else:
            assert type(channel) is tuple and len(channel) == 2

            self._handlers.add(handler)

            if channel not in self.channels:
                self.channels[channel] = []

            if handler not in self.channels[channel]:
                self.channels[channel].append(handler)
                self.channels[channel].sort(key=_sortkey)
                self.channels[channel].reverse()

            (target, channel) = channel

            if target not in self._tmap:
                self._tmap[target] = []
            if handler not in self._tmap[target]:
                self._tmap[target].append(handler)

            if channel not in self._cmap:
                self._cmap[channel] = []
            if handler not in self._cmap[channel]:
                self._cmap[channel].append(handler)

    def _remove(self, handler, channel=None):
        """E._remove(handler, channel=None) -> None

        Remove the given Event Handler from the Event Manager
        removing it from the given channel. if channel is None,
        remove it from all channels. This will succeed even
        if the specified  handler has already been removed.
        """

        if channel is None:
            if handler in self._globals:
                self._globals.remove(handler)
            channels = self.channels.keys()
        else:
            channels = [channel]

        if handler in self._handlers:
            self._handlers.remove(handler)

        for channel in channels:
            if handler in self.channels[channel]:
                self.channels[channel].remove(handler)
            if not self.channels[channel]:
                del self.channels[channel]

            (target, channel) = channel

            if target in self._tmap and handler in self._tmap:
                self._tmap[target].remove(handler)
                if not self._tmap[target]:
                    del self._tmap[target]

            if channel in self._cmap and handler in self._cmap:
                self._cmap[channel].remove(handler)
                if not self._cmap[channel]:
                    del self._cmap[channel]

    def _push(self, event, channel):
        self._queue.append((event, channel))

    def push(self, event, channel=None, target=None):
        """Push a new Event into the queue

        This will push the given Event, Channel and Target onto the
        Event Queue for later processing.

        if target is None, then target will be set as the Channel of
        the current Component, self.channel (defaulting back to None).

        If this Component's Manager is itself, enqueue on this Component's
        Event Queue, otherwise enqueue on this Component's Manager.

        @param event: The Event Object
        @type  event: Event

        @param channel: The Channel this Event is bound for
        @type  channel: str

        @keyword target: The target Component's channel this Event is bound for
        @type    target: str or Component
        """

        channel = channel or event.channel or event.name.lower()
        target = target if target is not None else event.target
        if isinstance(target, Component):
            target = getattr(target, "channel", "*")
        else:
            target = target or getattr(self, "channel", "*")

        event.channel = (target, channel)

        self.root._push(event, (target, channel))

    def _flush(self):
        q = self._queue
        self._queue = deque()
        while q: self._send(*q.popleft())

    def flush(self):
        """Flush all Events in the Event Queue

        This will flush all Events in the Event Queue. If this Component's
        Manager is itself, flush all Events from this Component's Event Queue,
        otherwise, flush all Events from this Component's Manager's Event Queue.
        """

        self.root._flush()

    def _send(self, event, channel, errors=False, log=True):
        eargs = event.args
        ekwargs = event.kwargs

        r = False
        for handler in self._getHandlers(channel):
            try:
                #stime = time.time()
                if handler._passEvent:
                    r = handler(event, *eargs, **ekwargs)
                else:
                    r = handler(*eargs, **ekwargs)
                #etime = time.time()
                #ttime = (etime - stime) * 1e3
                #print "%s: %0.02f ms" % (reprhandler(handler), ttime)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                if log:
                    etype, evalue, etraceback = _exc_info()
                    self.push(Error(etype, evalue, etraceback, handler=handler))
                if errors:
                    raise
                else:
                    _exc_clear()
            if r is not None and r and handler.filter:
                return r
        return r

    def send(self, event, channel=None, target=None, errors=False, log=True):
        """Send a new Event to Event Handlers for the Target and Channel

        This will send the given Event, to the spcified CHannel on the
        Target Component's Channel.

        if target is None, then target will be set as the Channel of
        the current Component, self.channel (defaulting back to None).

        If this Component's Manager is itself, enqueue on this Component's
        Event Queue, otherwise enqueue on this Component's Manager.

        @param event: The Event Object
        @type  event: Event

        @param channel: The Channel this Event is bound for
        @type  channel: str

        @keyword target: The target Component's channel this Event is bound for
        @type    target: str or Component

        @keyword errors: True to raise errors, False otherwise
        @type    errors: bool

        @keyword log: True to log errors, False otherwise
        @type    log: bool

        @return: The return value of the last executed Event Handler
        @rtype:  object
        """

        channel = channel or event.channel or event.name.lower()
        target = target if target is not None else event.target
        if isinstance(target, Component):
            target = getattr(target, "channel", "*")
        else:
            target = target or getattr(self, "channel", "*")

        event.channel = (target, channel)

        return self.root._send(event, (target, channel), errors, log)

    def _signal(self, signal, stack):
        if not self.send(Signal(signal, stack), "signal"):
            if signal == SIGINT:
                raise KeyboardInterrupt
            elif signal == SIGTERM:
                raise SystemExit

    def start(self, sleep=0, log=True, process=False):
        group = None
        target = self.run
        name = self.__class__.__name__
        mode = "P" if process else "T"
        args = (sleep, mode, log,)

        if process and HAS_MULTIPROCESSING:
            args += (self,)
            self._task = Process(group, target, name, args)
            setattr(self._task, "isAlive", self._task.is_alive)
            self._task.start()
            return

        self._task = Thread(group, target, name, args)
        self._task.setDaemon(True)
        self._task.start()

    def join(self, timeout=None):
        if hasattr(self._task, "join"):
            self._task.join(timeout)

    def stop(self):
        self._running = False
        if hasattr(self._task, "terminate"):
            self._task.terminate()
        if hasattr(self._task, "join"):
            self._task.join(3)
        self._task = None

    def _terminate(self):
        if HAS_MULTIPROCESSING:
            for p in processes():
                if not p == process():
                    p.terminate()
                    p.join(3)

    def run(self, sleep=0, mode=None, log=True, __self=None):
        if __self is not None:
            self = __self

        if not mode == "T":
            if os.name == "posix":
                signal(SIGHUP, self._signal)
            signal(SIGINT, self._signal)
            signal(SIGTERM, self._signal)

        self._running = True

        self.push(Started(self, mode))

        try:
            while self.running:
                try:
                    [f() for f in self._ticks.copy()]
                    self._flush()
                    if sleep:
                        try:
                            time.sleep(sleep)
                        except:
                            pass
                except (KeyboardInterrupt, SystemExit):
                    self._running = False
                except:
                    try:
                        if log:
                            self.push(Error(*_exc_info()))
                    finally:
                        self._flush()
        finally:
            try:
                self.push(Stopped(self))
                rtime = time.time()
                while len(self) > 0 and (time.time() - rtime) < 3:
                    try:
                        [f() for f in self._ticks.copy()]
                        self._flush()
                        if sleep:
                            time.sleep(sleep)
                        rtime = time.time()
                    except:
                        try:
                            if log:
                                self.push(Error(*_exc_info()))
                        finally:
                            self._flush()
            except:
                pass

class BaseComponent(Manager):
    """Base Component

    This is the Base of the Component which manages registrations to other
    components or managers. Every Base Component and thus Component has a
    unique Channel that is used as a separation of concern for it's registered
    Event Handlers. By default, this Channels is None (or also known as the
    Global Channel).

    When a Component (Base Component) has a set Channel that is not the Global
    Channel (None), then any Event Handlers will actually listen on a Channel
    that is a combination of the Component's Channel prefixed with the Event
    Handler's Channel. The form becomes:

    C{target:channel}

    Where:
       - target is the Component's Channel
       - channel is the Event Handler's Channel

    @ivar channel: The Component's Channel
    """

    channel = "*"

    def __new__(cls, *args, **kwargs):
        """TODO Work around for Python bug.

        Bug: http://bugs.python.org/issue5322
        """

        return object.__new__(cls)

    def __init__(self, *args, **kwargs):
        "initializes x; see x.__class__.__doc__ for signature"

        super(BaseComponent, self).__init__(*args, **kwargs)

        self.channel = kwargs.get("channel", self.channel) or "*"
        self.register(self)

    def __repr__(self):
        "x.__repr__() <==> repr(x)"

        name = self.__class__.__name__
        channel = self.channel or ""
        q = len(self._queue)
        c = len(self.channels)
        h = len(self._handlers)
        state = self.state
        format = "<%s/%s (q: %d c: %d h: %d) [%s]>"
        return format % (name, channel, q, c, h, state)

    def _registerHandlers(self, manager):
        p = lambda x: callable(x) and getattr(x, "handler", False)
        handlers = [v for k, v in getmembers(self, p)]

        for handler in handlers:
            if handler.channels:
                channels = handler.channels
            else:
                channels = [None]

            for channel in channels:
                if handler.target is not None:
                    target = handler.target
                else:
                    target = getattr(self, "channel", None)
                if not all([channel, target]):
                    channel = None
                else:
                    channel = (target, channel or "*")
                manager._add(handler, channel)

    def _unregisterHandlers(self, manager):
        for handler in self._handlers.copy():
            manager._remove(handler)

    def register(self, manager):
        """Register all Event Handlers with the given Manager
        
        This will register all Event Handlers of this Component to the
        given Manager. By default, every Component (Base Component) is
        registered with itself.
        
        Iif the Component or Manager being registered
        with is not the current Component, then any Hidden Components
        in registered to this Component will also be regsitered with the
        given Manager. A Registered Event will also be sent.
        """

        def _register(c, m, r):
            c._registerHandlers(m)
            c.root = r
            if c._queue:
                m._queue.extend(list(c._queue))
                c._queue.clear()
            if m is not r:
                c._registerHandlers(r)
                if m._queue:
                    r._queue.extend(list(m._queue))
                    m._queue.clear()
            if hasattr(c, "__tick__"):
                m._ticks.add(getattr(c, "__tick__"))
                if m is not r:
                    r._ticks.add(getattr(c, "__tick__"))
            for x in c.components:
                _register(x, m, r)

        _register(self, manager, findroot(manager))

        self.manager = manager

        if manager is not self:
            manager.components.add(self)
            self.push(Registered(self, manager), target=self)

    def unregister(self):
        """Unregister all registered Event Handlers
        
        This will unregister all registered Event Handlers of this Component
        from it's registered Component or Manager.

        @note: It's possible to unregister a Component from itself!
        """

        def _unregister(c, m, r):
            c._unregisterHandlers(m)
            c.root = self
            if m is not r:
                c._unregisterHandlers(r)
            if hasattr(c, "__tick__"):
                m._ticks.remove(getattr(c, "__tick__"))
                if m is not r:
                    r._ticks.remove(getattr(c, "__tick__"))

            for x in c.components:
                _unregister(x, m, r)

        self.push(Unregistered(self, self.manager), target=self)

        root = findroot(self.manager)
        _unregister(self, self.manager, root)

        self.manager.components.remove(self)
        self.push(Unregistered(self, self.manager), target=self)

        self.manager = self

class Component(BaseComponent):
    "Component"

    __metaclass__ = HandlersType

    def __new__(cls, *args, **kwargs):
        self = BaseComponent.__new__(cls, *args, **kwargs)
        handlers = [x for x in cls.__dict__.values() \
                if getattr(x, "handler", False)]
        overridden = lambda x: [h for h in handlers \
                if x.channels == h.channels and getattr(h, "override", False)]
        for base in cls.__bases__:
            if issubclass(cls, base):
                for k, v in base.__dict__.items():
                    p1 = callable(v)
                    p2 = getattr(v, "handler", False)
                    predicate = p1 and p2 and not overridden(v)
                    if predicate:
                        name = "%s_%s" % (base.__name__, k)
                        method = new.instancemethod(v, self, cls)
                        setattr(self, name, method)
        return self




class Timer(Component):
    """Timer(s, e, c, t, persist) -> new timer component

    Creates a new timer object which when triggered
    will push the given event onto the event queue.

    s := no. of seconds to delay
    e := event to be fired
    c := channel to fire event to
    t := target to fire event to

    persist := Sets this timer as persistent if True.
    """

    def __init__(self, s, e, c="timer", t=None, persist=False):
        "initializes x; see x.__class__.__doc__ for signature"

        super(Timer, self).__init__()

        self.s = s
        self.e = e
        self.c = c
        self.t = t
        self.persist = persist

        self.reset()

    def __tick__(self):
        self.poll()

    def reset(self):
        """T.reset() -> None

        Reset the timer.
        """

        self._eTime = time() + self.s

    def poll(self):
        """T.poll() -> state

        Check if this timer is ready to be triggered.
        If so, push the event onto the event queue.

        If timer is persistent, reset it after triggering.
        """

        if time() > self._eTime:
            self.push(self.e, self.c, self.t)

            if self.persist:
                self.reset()
                return False
            else:
                self.unregister()
                return True

        return None

POLL_INTERVAL = 0.00001

# class Thread(BaseComponent):
#     def __init__(self, *args, **kwargs):
#         super(Thread, self).__init__(*args, **kwargs)
#         self._thread = _Thread(target=self.run)
#     def start(self):
#         self._running = True
#         self._thread.start()
#     def run(self):
#         pass
#     def stop(self):
#         self._running = False
#     def join(self):
#         return self._thread.join()
#     @property
#     def alive(self):
#         return self.running and self._thread.isAlive()

class Process(BaseComponent):
    def __init__(self, *args, **kwargs):
        super(Process, self).__init__(*args, **kwargs)
        self._running = _Value("b", False)
        self.process = _Process(target=self._run, args=(self.run, self._running,))
        self.parent, self.child = _Pipe()
        
    def _run(self, fn, running):
        thread = Thread(target=fn)
        thread.start()        
        try:
            while running.value:
                try:
                    self.flush()
                    if self.child.poll(POLL_INTERVAL):
                        event = self.child.recv()
                        channel = event.channel
                        target = event.target
                        self.send(event, channel, target)
                except SystemExit:
                    running.acquire()
                    running.value = False
                    running.release()
                    break
                except KeyboardInterrupt:
                    running.acquire()
                    running.value = False
                    running.release()
                    break
        finally:
            running.acquire()
            running.value = False
            running.release()
            thread.join()
            self.flush()
                
    def start(self):
        self._running.acquire()
        self._running.value = True
        self._running.release()
        self.process.start()
        
    def run(self):
        pass

    def stop(self):
        self._running.acquire()
        self._running.value = False
        self._running.release()

    def isAlive(self):
        return self._running.value

    def poll(self, wait=POLL_INTERVAL):
        if self.parent.poll(POLL_INTERVAL):
            event = self.parent.recv()
            channel = event.channel
            target = event.target
            self.send(event, channel, target)

def walk(x, f, d=0, v=None):
    if not v:
        v = set()
    yield f(d, x)
    for c in x.components.copy():
        if c not in v:
            v.add(c)
            for r in walk(c, f, d + 1, v):
                yield r

def edges(x, e=None, v=None):
    if not e:
        e = set()
    if not v:
        v = set()
    for c in x.components.copy():
        if c not in v:
            v.add(c)
            e.add((x, c))
            edges(c, e, v)
    return e

def findroot(x, v=None):
    if not v:
        v = set()
    if x.manager == x:
        return x
    else:
        if x.manager not in v:
            v.add(x.manager)
            return findroot(x.manager, v)
        else:
            return x.manager

def kill(x):
    for c in x.components.copy():
        kill(c)
    if x.manager != x:
        x.unregister()

def graph(x, name=None):
    """Display a directed graph of the Component structure of x

    @param x: A Component or Manager to graph
    @type  x: Component or Manager

    @param name: A name for the graph (defaults to x's name)
    @type  name: str

    @return: A directed graph representing x's Component sturcture.
    @rtype:  str
    """

    try:
        import pydot
        
        graph_edges = []
        nodes = []
        names = []
        for (u, v) in edges(x):
            if v.name in names and v not in nodes:
                i = 1
                new_name = "%s-%d" % (v.name, i)
                while new_name in names:
                    i += 1
                    new_name = "%s-%d" % (v.name, i)
                graph_edges.append((u.name, new_name))
            else:
                nodes.append(u)
                nodes.append(v)
                names.append(v.name)
                graph_edges.append((u.name, v.name))

        g = pydot.graph_from_edges(graph_edges, directed=True)
        g.write("%s.dot" % (name or x.name))
        g.write("%s.png" % (name or x.name), format="png")
    except ImportError:
        pass
    except:
        raise

    def printer(d, x):
        return "%s* %s" % (" " * d, x)

    return "\n".join(walk(x, printer))
    
def reprhandler(x):
    """Display a nicely formatted Event Handler, x

    @param x: An Event Handler
    @type  x: function or method

    @return: A nicely formatted representation of the Event Handler, x
    @rtype:  str
    """

    if not hasattr(x, "handler"):
        raise TypeError("%r is not an Event Handler" % x)

    format = "<handler (%s) {f: %s, t: %r, p: %d}>"
    channels = ",".join(x.channels)
    f = x.filter
    t = x.target or ""
    p = x.priority
    return format % (channels, f, t, p)

def inspect(x):
    """Display an inspection report of the Component or Manager x

    @param x: A Component or Manager to graph
    @type  x: Component or Manager

    @return: A detailed inspection report of x
    @rtype:  str
    """

    s = []
    write = s.append

    write(" Registered Components: %d\n" % len(x.components))
    for component in x.components:
        write("  %s\n" % component)
    write("\n")

    write(" Tick Functions: %d\n" % len(x._ticks))
    for tick in x._ticks:
        write("  %s\n" % tick)
    write("\n")

    write(" Channels and Event Handlers: %d\n" % len(x.channels))
    for (t, c) in x.channels:
        write("  %s:%s; %d\n" % (t, c, len(x.channels[(t, c)])))
        for handler in x.channels[(t, c)]:
            write("   %s\n" % reprhandler(handler))

    return "".join(s)

#else:
#    Process = Thread

MASK = ALL_EVENTS

class Moved(Event): pass
class Opened(Event): pass
class Closed(Event): pass
class Created(Event): pass
class Deleted(Event): pass
class Accessed(Event): pass
class Modified(Event): pass
class Unmounted(Event): pass

EVENT_MAP = {
        IN_MOVED_TO:        Moved,
        IN_MOVE_SELF:       Moved,
        IN_MOVED_FROM:      Moved,
        IN_CLOSE_WRITE:     Closed,
        IN_CLOSE_NOWRITE:   Closed,
        IN_OPEN:            Opened,
        IN_DELETE_SELF:     Deleted,
        IN_DELETE:          Deleted,
        IN_CREATE:          Created,
        IN_ACCESS:          Accessed,
        IN_MODIFY:          Modified,
        IN_ATTRIB:          Modified,
        IN_UNMOUNT:         Unmounted}

class INotifyDriver(Component):
    channel = "inotify"
    def __init__(self, freq=1, timeout=1, channel=channel):
        super(INotifyDriver, self).__init__(channel=channel)

        self._freq = freq
        self._wm = WatchManager()
        self._notifier = Notifier(self._wm, self._process, timeout=timeout)

    def _sleep(self, rtime):
        # Only consider sleeping if _freq is > 0
        if self._freq > 0:
            ctime = time.time()
            s = self._freq - (ctime - rtime)
            if s > 0:
                time.sleep(s)

    def __tick__(self):
        self._notifier.process_events()
        rtime = time.time()
        if self._notifier.check_events():
            self._sleep(rtime)
            self._notifier.read_events()

    def _process(self, event):
        dir = event.dir
        mask = event.mask
        path = event.path
        name = event.name
        pathname = event.pathname
        print mask, path, name, dir, pathname
        
        for k, v in EVENT_MAP.iteritems():
            if mask & k:
                e = v(name, path, pathname, dir)
                c = e.name.lower()
                self.push(e, c)

    def add(self, path, mask=None, recursive=False):
        mask = mask or MASK
        self._wm.add_watch(path, mask, rec=recursive)

    def remove(self, path, recursive=False):
        wd = self._wm.get_wd(path)
        if wd:
            self._wm.rm_watch(wd, rec=recursive)
