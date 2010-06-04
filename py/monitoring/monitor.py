import sys
import core.plugins.pattern_threaded as threaded

class basic_monitor(threaded.threading_pattern):
    def __init__(self):
        self.test = "test data"

    def hi(self):
        return "hi"
