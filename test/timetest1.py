class Foo():
  def bar(self):
    self.private_a = 4
    return self.private_a



x = Foo()

for i in range(1,1000000):
  x.bar()

    
