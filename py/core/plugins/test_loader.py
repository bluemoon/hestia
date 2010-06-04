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
    """    
    def test_1_load_module(self):
        self.loader.load_module('example_plugin')

    def test_repr(self):
        self.assertTrue(repr(self.loader).startswith('<Loader'))

    def test_get_modules(self):
        assert self.loader.get_modules
        
    def test_get_classes(self):
        assert self.loader.get_classes

    def test_get_class_instances(self):
        assert self.loader.get_class_instances

    def test_get_module(self):
        assert self.loader.get_module('example_plugin')

    def test_get_function(self):
        assert self.loader.get_function
        
    def test_system_loaded_module(self):
        assert self.loader.system_loaded_module('unittest')

    def test_load_module_fail(self):
        self.failUnlessRaises(ImportError, self.loader.load_module, 'gidjgiajd')

    def test_get_instance(self):
        t = self.loader.get_instance('py.core.plugins.example_plugin')
        self.assertTrue(t.example1.true() == True)

    """
