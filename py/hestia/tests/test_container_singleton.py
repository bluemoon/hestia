import unittest
from all import *

class Dummy(Singleton):
    pass

class Dummy2(Dummy):
    pass

class Dummy3(Dummy2):
    pass

class TestContainerSingleton(unittest.TestCase):
    def setUp(self):
        self.single = Dummy()
        
    def test_with_dummy_class(self):
        dummy2 = Dummy()
        dummy2.data = 3.4

        self.assertTrue(dummy2.data == self.single.data)
        
    def test_dummy2_class(self):
        d1 = Dummy2()
        d2 = Dummy2()

        d1.x = 3
        self.assertTrue(d2.x == 3)
        
    def test_dummy3_class(self):
        d1 = Dummy3()
        d2 = Dummy3()
        d3 = Dummy()
        
        d1.x = 3
        
        self.assertTrue(d2.x == 3)
        self.assertTrue(d3.x == 3)

        d3.x = 5
        
        self.assertTrue(d2.x == 5)
        self.assertTrue(d1.x == 5)
        self.assertEquals(id(d1), id(d2))
