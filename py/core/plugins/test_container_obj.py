import unittest
import container_obj

class TestObj(unittest.TestCase):
    def setUp(self):
        d = {'a': 1, 'b': {'c': 2}, 'd': ["hi", {'foo': "bar"}]}
        self.object = container_obj.Obj(d)
        
    def test_obj_1_depth(self):
        self.assertTrue(self.object.a == 1)

    def test_obj_2_depth(self):
        self.assertTrue(self.object.b.c == 2)

    def test_object_proxy_basic_test_1(self):
        uni = container_obj.ObjectProxy()
        uni.a.b.c = 3
        self.assertTrue(uni.a.b.c == 3)

    def test_object_proxy_basic_test_2(self):
        uni = container_obj.ObjectProxy()
        uni.a.b.c = 3
        uni.a.b.d = 6
        self.assertTrue(uni.a.b.d == 6)
        self.assertTrue(uni.a.b.c == 3)

        #pass
