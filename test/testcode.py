import unittest

class Foo():
  def set(self, a):
    self.private_a = a
  def get(self):
    return self.private_a

class TestFoo(unittest.TestCase):
  def setUp(self):
    self.x = Foo()

  def test_get_none(self):
    self.assertEqual(self.x.get(), None)

  def test_set_get(self):
    self.x.set(4)
    self.assertEqual(self.x.get(), 4)

  def test_set_set_get(self):    
    self.x.set(4)
    self.x.set(5)
    self.assertEqual(self.x.get(), 5)

if __name__ == '__main__':
  unittest.main()
