import unittest
import loader
import os

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.loader = loader.loader()
        
    def test_has_attr_class(self):
        assert hasattr(self.loader, 'module_classes')

    def test_attr_same(self):
        new_loader = loader.loader()
        self.loader.module_classes['d'] = True
        assert self.loader.module_classes['d'] == new_loader.module_classes['d']
        
    def test_load_module(self):
        self.loader.load_module('example_plugin')
        #assert False
