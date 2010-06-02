import unittest
import loader

class TestLoader(unittest.TestCase):
    def setUp(self):
        self.loader = loader.loader()

    def test_has_attr_class(self):
        assert hasattr(self.loader, 'classes')

    def test_attr_same(self):
        new_loader = loader.loader()
        self.loader.classes['d'] = True
        assert self.loader.classes['d'] == new_loader.classes['d']
