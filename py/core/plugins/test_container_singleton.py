import unittest
import container_singleton

class Dummy(container_singleton.Singleton):
    pass

class TestContainerSingleton(unittest.TestCase):
    def setUp(self):
        self.single = Dummy()
        
    def test_with_dummy_class(self):
        dummy2 = Dummy()
        dummy2.data = 3.4

        self.assertTrue(dummy2.data == self.single.data)
        
