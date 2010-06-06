import all
from nose.tools import assert_equal
from nose import SkipTest

class TestEvent:
    def test___eq__(self):
        # event = Event(*args, **kwargs)
        # assert_equal(expected, event.__eq__(other))
        raise SkipTest # TODO: implement your test here

    def test___getitem__(self):
        # event = Event(*args, **kwargs)
        # assert_equal(expected, event.__getitem__(x))
        raise SkipTest # TODO: implement your test here

    def test___init__(self):
        # event = Event(*args, **kwargs)
        raise SkipTest # TODO: implement your test here

    def test___repr__(self):
        # event = Event(*args, **kwargs)
        # assert_equal(expected, event.__repr__())
        raise SkipTest # TODO: implement your test here

    def test_name(self):
        # event = Event(*args, **kwargs)
        # assert_equal(expected, event.name())
        raise SkipTest # TODO: implement your test here

class TestError:
    def test___init__(self):
        # error = Error(type, value, traceback, **kwargs)
        raise SkipTest # TODO: implement your test here

class TestStarted:
    def test___init__(self):
        # started = Started(component, mode)
        raise SkipTest # TODO: implement your test here

class TestStopped:
    def test___init__(self):
        # stopped = Stopped(component)
        raise SkipTest # TODO: implement your test here

class TestSignal:
    def test___init__(self):
        # signal = Signal(signal, stack)
        raise SkipTest # TODO: implement your test here

class TestRegistered:
    def test___init__(self):
        # registered = Registered(component, manager)
        raise SkipTest # TODO: implement your test here

class TestUnregistered:
    def test___init__(self):
        # unregistered = Unregistered(component, manager)
        raise SkipTest # TODO: implement your test here

class TestHandler:
    def test_handler(self):
        # assert_equal(expected, handler(*channels, **kwargs))
        raise SkipTest # TODO: implement your test here

class TestHandlersType:
    def test___init__(self):
        # handlers_type = HandlersType(name, bases, dct)
        raise SkipTest # TODO: implement your test here

class TestManager:
    def test___add__(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.__add__(y))
        raise SkipTest # TODO: implement your test here

    def test___iadd__(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.__iadd__(y))
        raise SkipTest # TODO: implement your test here

    def test___init__(self):
        # manager = Manager(*args, **kwargs)
        raise SkipTest # TODO: implement your test here

    def test___isub__(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.__isub__(y))
        raise SkipTest # TODO: implement your test here

    def test___len__(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.__len__())
        raise SkipTest # TODO: implement your test here

    def test___repr__(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.__repr__())
        raise SkipTest # TODO: implement your test here

    def test___sub__(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.__sub__(y))
        raise SkipTest # TODO: implement your test here

    def test_flush(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.flush())
        raise SkipTest # TODO: implement your test here

    def test_join(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.join(timeout))
        raise SkipTest # TODO: implement your test here

    def test_name(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.name())
        raise SkipTest # TODO: implement your test here

    def test_push(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.push(event, channel, target))
        raise SkipTest # TODO: implement your test here

    def test_run(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.run(sleep, mode, log, __self))
        raise SkipTest # TODO: implement your test here

    def test_running(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.running())
        raise SkipTest # TODO: implement your test here

    def test_send(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.send(event, channel, target, errors, log))
        raise SkipTest # TODO: implement your test here

    def test_start(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.start(sleep, log, process))
        raise SkipTest # TODO: implement your test here

    def test_state(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.state())
        raise SkipTest # TODO: implement your test here

    def test_stop(self):
        # manager = Manager(*args, **kwargs)
        # assert_equal(expected, manager.stop())
        raise SkipTest # TODO: implement your test here

class TestBaseComponent:
    def test___init__(self):
        # base_component = BaseComponent(*args, **kwargs)
        raise SkipTest # TODO: implement your test here

    def test___new__(self):
        # base_component = BaseComponent(*args, **kwargs)
        raise SkipTest # TODO: implement your test here

    def test___repr__(self):
        # base_component = BaseComponent(*args, **kwargs)
        # assert_equal(expected, base_component.__repr__())
        raise SkipTest # TODO: implement your test here

    def test_register(self):
        # base_component = BaseComponent(*args, **kwargs)
        # assert_equal(expected, base_component.register(manager))
        raise SkipTest # TODO: implement your test here

    def test_unregister(self):
        # base_component = BaseComponent(*args, **kwargs)
        # assert_equal(expected, base_component.unregister())
        raise SkipTest # TODO: implement your test here

class TestComponent:
    def test___new__(self):
        # component = Component(*args, **kwargs)
        raise SkipTest # TODO: implement your test here

class TestTimer:
    def test___init__(self):
        # timer = Timer(s, e, c, t, persist)
        raise SkipTest # TODO: implement your test here

    def test___tick__(self):
        # timer = Timer(s, e, c, t, persist)
        # assert_equal(expected, timer.__tick__())
        raise SkipTest # TODO: implement your test here

    def test_poll(self):
        # timer = Timer(s, e, c, t, persist)
        # assert_equal(expected, timer.poll())
        raise SkipTest # TODO: implement your test here

    def test_reset(self):
        # timer = Timer(s, e, c, t, persist)
        # assert_equal(expected, timer.reset())
        raise SkipTest # TODO: implement your test here

class TestProcess:
    def test___init__(self):
        # process = Process(*args, **kwargs)
        raise SkipTest # TODO: implement your test here

    def test_isAlive(self):
        # process = Process(*args, **kwargs)
        # assert_equal(expected, process.isAlive())
        raise SkipTest # TODO: implement your test here

    def test_poll(self):
        # process = Process(*args, **kwargs)
        # assert_equal(expected, process.poll(wait))
        raise SkipTest # TODO: implement your test here

    def test_run(self):
        # process = Process(*args, **kwargs)
        # assert_equal(expected, process.run())
        raise SkipTest # TODO: implement your test here

    def test_start(self):
        # process = Process(*args, **kwargs)
        # assert_equal(expected, process.start())
        raise SkipTest # TODO: implement your test here

    def test_stop(self):
        # process = Process(*args, **kwargs)
        # assert_equal(expected, process.stop())
        raise SkipTest # TODO: implement your test here

