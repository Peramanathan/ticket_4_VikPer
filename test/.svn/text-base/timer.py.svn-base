def test1():
  class Foo():
    def bar(self):
      self.private_a = 4
      return self.private_a
  x = Foo()
  x.bar()

def test2():
  class Foo():
    def bar(self):
      self.public_a = 4
      return self.public_a
  x = Foo()
  x.bar()

if __name__ == '__main__':
    from timeit import Timer
    t1 = Timer("test1()")
    t2 = Timer("test2()")
    print t1.timeit()
    print t2.timeit()



t1 = timeit.Timer('global x;x.func1();x.func3()')
t2 = timeit.Timer('x.func2();x.func4()')

t1.timeit()
t2.timeit()
