from circuits.core import Event

class E(Event): 
    def __init__(self, *args, **kwargs):
        super(E, self).__init__(*args, **kwargs)
        #self.channel = self.__class__.__name__

class Notification(E):
    pass

class cmd_run(E):
    pass

class returncode(E): 
    pass

