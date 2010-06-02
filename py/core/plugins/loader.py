from container_singleton import Singleton

class loader(Singleton):
    def __init__(self):
        self.classes = {}
        self.modules = {}
        
    def add_class(self, class_name):
        pass
    def add_module(self, module):
        pass
    
