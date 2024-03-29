:tocdepth: 2

===============
Programming FAQ
===============

.. contents::

General Questions
=================

Is there a source code level debugger with breakpoints, single-stepping, etc.?
------------------------------------------------------------------------------

Yes.

The pdb module is a simple but adequate console-mode debugger for Python. It is
part of the standard Python library, and is :mod:`documented in the Library
Reference Manual <pdb>`. You can also write your own debugger by using the code
for pdb as an example.

The IDLE interactive development environment, which is part of the standard
Python distribution (normally available as Tools/scripts/idle), includes a
graphical debugger.  There is documentation for the IDLE debugger at
http://www.python.org/idle/doc/idle2.html#Debugger.

PythonWin is a Python IDE that includes a GUI debugger based on pdb.  The
Pythonwin debugger colors breakpoints and has quite a few cool features such as
debugging non-Pythonwin programs.  Pythonwin is available as part of the `Python
for Windows Extensions <http://sourceforge.net/projects/pywin32/>`__ project and
as a part of the ActivePython distribution (see
http://www.activestate.com/Products/ActivePython/index.html).

`Boa Constructor <http://boa-constructor.sourceforge.net/>`_ is an IDE and GUI
builder that uses wxWidgets.  It offers visual frame creation and manipulation,
an object inspector, many views on the source like object browsers, inheritance
hierarchies, doc string generated html documentation, an advanced debugger,
integrated help, and Zope support.

`Eric <http://www.die-offenbachs.de/eric/index.html>`_ is an IDE built on PyQt
and the Scintilla editing component.

Pydb is a version of the standard Python debugger pdb, modified for use with DDD
(Data Display Debugger), a popular graphical debugger front end.  Pydb can be
found at http://bashdb.sourceforge.net/pydb/ and DDD can be found at
http://www.gnu.org/software/ddd.

There are a number of commercial Python IDEs that include graphical debuggers.
They include:

* Wing IDE (http://wingware.com/)
* Komodo IDE (http://www.activestate.com/Products/Komodo)


Is there a tool to help find bugs or perform static analysis?
-------------------------------------------------------------

Yes.

PyChecker is a static analysis tool that finds bugs in Python source code and
warns about code complexity and style.  You can get PyChecker from
http://pychecker.sf.net.

`Pylint <http://www.logilab.org/projects/pylint>`_ is another tool that checks
if a module satisfies a coding standard, and also makes it possible to write
plug-ins to add a custom feature.  In addition to the bug checking that
PyChecker performs, Pylint offers some additional features such as checking line
length, whether variable names are well-formed according to your coding
standard, whether declared interfaces are fully implemented, and more.
http://www.logilab.org/card/pylint_manual provides a full list of Pylint's
features.


How can I create a stand-alone binary from a Python script?
-----------------------------------------------------------

You don't need the ability to compile Python to C code if all you want is a
stand-alone program that users can download and run without having to install
the Python distribution first.  There are a number of tools that determine the
set of modules required by a program and bind these modules together with a
Python binary to produce a single executable.

One is to use the freeze tool, which is included in the Python source tree as
``Tools/freeze``. It converts Python byte code to C arrays; a C compiler you can
embed all your modules into a new program, which is then linked with the
standard Python modules.

It works by scanning your source recursively for import statements (in both
forms) and looking for the modules in the standard Python path as well as in the
source directory (for built-in modules).  It then turns the bytecode for modules
written in Python into C code (array initializers that can be turned into code
objects using the marshal module) and creates a custom-made config file that
only contains those built-in modules which are actually used in the program.  It
then compiles the generated C code and links it with the rest of the Python
interpreter to form a self-contained binary which acts exactly like your script.

Obviously, freeze requires a C compiler.  There are several other utilities
which don't. One is Thomas Heller's py2exe (Windows only) at

    http://www.py2exe.org/

Another is Christian Tismer's `SQFREEZE <http://starship.python.net/crew/pirx>`_
which appends the byte code to a specially-prepared Python interpreter that can
find the byte code in the executable.

Other tools include Fredrik Lundh's `Squeeze
<http://www.pythonware.com/products/python/squeeze>`_ and Anthony Tuininga's
`cx_Freeze <http://starship.python.net/crew/atuining/cx_Freeze/index.html>`_.


Are there coding standards or a style guide for Python programs?
----------------------------------------------------------------

Yes.  The coding style required for standard library modules is documented as
:pep:`8`.


My program is too slow. How do I speed it up?
---------------------------------------------

That's a tough one, in general.  There are many tricks to speed up Python code;
consider rewriting parts in C as a last resort.

In some cases it's possible to automatically translate Python to C or x86
assembly language, meaning that you don't have to modify your code to gain
increased speed.

.. XXX seems to have overlap with other questions!

`Pyrex <http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/>`_ can compile a
slightly modified version of Python code into a C extension, and can be used on
many different platforms.

`Psyco <http://psyco.sourceforge.net>`_ is a just-in-time compiler that
translates Python code into x86 assembly language.  If you can use it, Psyco can
provide dramatic speedups for critical functions.

The rest of this answer will discuss various tricks for squeezing a bit more
speed out of Python code.  *Never* apply any optimization tricks unless you know
you need them, after profiling has indicated that a particular function is the
heavily executed hot spot in the code.  Optimizations almost always make the
code less clear, and you shouldn't pay the costs of reduced clarity (increased
development time, greater likelihood of bugs) unless the resulting performance
benefit is worth it.

There is a page on the wiki devoted to `performance tips
<http://wiki.python.org/moin/PythonSpeed/PerformanceTips>`_.

Guido van Rossum has written up an anecdote related to optimization at
http://www.python.org/doc/essays/list2str.html.

One thing to notice is that function and (especially) method calls are rather
expensive; if you have designed a purely OO interface with lots of tiny
functions that don't do much more than get or set an instance variable or call
another method, you might consider using a more direct way such as directly
accessing instance variables.  Also see the standard module :mod:`profile` which
makes it possible to find out where your program is spending most of its time
(if you have some patience -- the profiling itself can slow your program down by
an order of magnitude).

Remember that many standard optimization heuristics you may know from other
programming experience may well apply to Python.  For example it may be faster
to send output to output devices using larger writes rather than smaller ones in
order to reduce the overhead of kernel system calls.  Thus CGI scripts that
write all output in "one shot" may be faster than those that write lots of small
pieces of output.

Also, be sure to use Python's core features where appropriate.  For example,
slicing allows programs to chop up lists and other sequence objects in a single
tick of the interpreter's mainloop using highly optimized C implementations.
Thus to get the same effect as::

   L2 = []
   for i in range(3):
       L2.append(L1[i])

it is much shorter and far faster to use ::

   L2 = list(L1[:3])  # "list" is redundant if L1 is a list.

Note that the functionally-oriented built-in functions such as :func:`map`,
:func:`zip`, and friends can be a convenient accelerator for loops that
perform a single task.  For example to pair the elements of two lists
together::

   >>> zip([1, 2, 3], [4, 5, 6])
   [(1, 4), (2, 5), (3, 6)]

or to compute a number of sines::

   >>> map(math.sin, (1, 2, 3, 4))
   [0.841470984808, 0.909297426826, 0.14112000806, -0.756802495308]

The operation completes very quickly in such cases.

Other examples include the ``join()`` and ``split()`` :ref:`methods
of string objects <string-methods>`.
For example if s1..s7 are large (10K+) strings then
``"".join([s1,s2,s3,s4,s5,s6,s7])`` may be far faster than the more obvious
``s1+s2+s3+s4+s5+s6+s7``, since the "summation" will compute many
subexpressions, whereas ``join()`` does all the copying in one pass.  For
manipulating strings, use the ``replace()`` and the ``format()`` :ref:`methods
on string objects <string-methods>`.  Use regular expressions only when you're
not dealing with constant string patterns.  You may still use :ref:`the old %
operations <string-formatting>` ``string % tuple`` and ``string % dictionary``.

Be sure to use the :meth:`list.sort` built-in method to do sorting, and see the
`sorting mini-HOWTO <http://wiki.python.org/moin/HowTo/Sorting>`_ for examples
of moderately advanced usage.  :meth:`list.sort` beats other techniques for
sorting in all but the most extreme circumstances.

Another common trick is to "push loops into functions or methods."  For example
suppose you have a program that runs slowly and you use the profiler to
determine that a Python function ``ff()`` is being called lots of times.  If you
notice that ``ff()``::

   def ff(x):
       ... # do something with x computing result...
       return result

tends to be called in loops like::

   list = map(ff, oldlist)

or::

   for x in sequence:
       value = ff(x)
       ... # do something with value...

then you can often eliminate function call overhead by rewriting ``ff()`` to::

   def ffseq(seq):
       resultseq = []
       for x in seq:
           ... # do something with x computing result...
           resultseq.append(result)
       return resultseq

and rewrite the two examples to ``list = ffseq(oldlist)`` and to::

   for value in ffseq(sequence):
       ... # do something with value...

Single calls to ``ff(x)`` translate to ``ffseq([x])[0]`` with little penalty.
Of course this technique is not always appropriate and there are other variants
which you can figure out.

You can gain some performance by explicitly storing the results of a function or
method lookup into a local variable.  A loop like::

   for key in token:
       dict[key] = dict.get(key, 0) + 1

resolves ``dict.get`` every iteration.  If the method isn't going to change, a
slightly faster implementation is::

   dict_get = dict.get  # look up the method once
   for key in token:
       dict[key] = dict_get(key, 0) + 1

Default arguments can be used to determine values once, at compile time instead
of at run time.  This can only be done for functions or objects which will not
be changed during program execution, such as replacing ::

   def degree_sin(deg):
       return math.sin(deg * math.pi / 180.0)

with ::

   def degree_sin(deg, factor=math.pi/180.0, sin=math.sin):
       return sin(deg * factor)

Because this trick uses default arguments for terms which should not be changed,
it should only be used when you are not concerned with presenting a possibly
confusing API to your users.


Core Language
=============

Why am I getting an UnboundLocalError when the variable has a value?
--------------------------------------------------------------------

It can be a surprise to get the UnboundLocalError in previously working
code when it is modified by adding an assignment statement somewhere in
the body of a function.

This code:

   >>> x = 10
   >>> def bar():
   ...     print x
   >>> bar()
   10

works, but this code:

   >>> x = 10
   >>> def foo():
   ...     print x
   ...     x += 1

results in an UnboundLocalError:

   >>> foo()
   Traceback (most recent call last):
     ...
   UnboundLocalError: local variable 'x' referenced before assignment

This is because when you make an assignment to a variable in a scope, that
variable becomes local to that scope and shadows any similarly named variable
in the outer scope.  Since the last statement in foo assigns a new value to
``x``, the compiler recognizes it as a local variable.  Consequently when the
earlier ``print x`` attempts to print the uninitialized local variable and
an error results.

In the example above you can access the outer scope variable by declaring it
global:

   >>> x = 10
   >>> def foobar():
   ...     global x
   ...     print x
   ...     x += 1
   >>> foobar()
   10

This explicit declaration is required in order to remind you that (unlike the
superficially analogous situation with class and instance variables) you are
actually modifying the value of the variable in the outer scope:

   >>> print x
   11


What are the rules for local and global variables in Python?
------------------------------------------------------------

In Python, variables that are only referenced inside a function are implicitly
global.  If a variable is assigned a new value anywhere within the function's
body, it's assumed to be a local.  If a variable is ever assigned a new value
inside the function, the variable is implicitly local, and you need to
explicitly declare it as 'global'.

Though a bit surprising at first, a moment's consideration explains this.  On
one hand, requiring :keyword:`global` for assigned variables provides a bar
against unintended side-effects.  On the other hand, if ``global`` was required
for all global references, you'd be using ``global`` all the time.  You'd have
to declare as global every reference to a built-in function or to a component of
an imported module.  This clutter would defeat the usefulness of the ``global``
declaration for identifying side-effects.


How do I share global variables across modules?
------------------------------------------------

The canonical way to share information across modules within a single program is
to create a special module (often called config or cfg).  Just import the config
module in all modules of your application; the module then becomes available as
a global name.  Because there is only one instance of each module, any changes
made to the module object get reflected everywhere.  For example:

config.py::

   x = 0   # Default value of the 'x' configuration setting

mod.py::

   import config
   config.x = 1

main.py::

   import config
   import mod
   print config.x

Note that using a module is also the basis for implementing the Singleton design
pattern, for the same reason.


What are the "best practices" for using import in a module?
-----------------------------------------------------------

In general, don't use ``from modulename import *``.  Doing so clutters the
importer's namespace.  Some people avoid this idiom even with the few modules
that were designed to be imported in this manner.  Modules designed in this
manner include :mod:`Tkinter`, and :mod:`threading`.

Import modules at the top of a file.  Doing so makes it clear what other modules
your code requires and avoids questions of whether the module name is in scope.
Using one import per line makes it easy to add and delete module imports, but
using multiple imports per line uses less screen space.

It's good practice if you import modules in the following order:

1. standard library modules -- e.g. ``sys``, ``os``, ``getopt``, ``re``
2. third-party library modules (anything installed in Python's site-packages
   directory) -- e.g. mx.DateTime, ZODB, PIL.Image, etc.
3. locally-developed modules

Never use relative package imports.  If you're writing code that's in the
``package.sub.m1`` module and want to import ``package.sub.m2``, do not just
write ``import m2``, even though it's legal.  Write ``from package.sub import
m2`` instead.  Relative imports can lead to a module being initialized twice,
leading to confusing bugs.  See :pep:`328` for details.

It is sometimes necessary to move imports to a function or class to avoid
problems with circular imports.  Gordon McMillan says:

   Circular imports are fine where both modules use the "import <module>" form
   of import.  They fail when the 2nd module wants to grab a name out of the
   first ("from module import name") and the import is at the top level.  That's
   because names in the 1st are not yet available, because the first module is
   busy importing the 2nd.

In this case, if the second module is only used in one function, then the import
can easily be moved into that function.  By the time the import is called, the
first module will have finished initializing, and the second module can do its
import.

It may also be necessary to move imports out of the top level of code if some of
the modules are platform-specific.  In that case, it may not even be possible to
import all of the modules at the top of the file.  In this case, importing the
correct modules in the corresponding platform-specific code is a good option.

Only move imports into a local scope, such as inside a function definition, if
it's necessary to solve a problem such as avoiding a circular import or are
trying to reduce the initialization time of a module.  This technique is
especially helpful if many of the imports are unnecessary depending on how the
program executes.  You may also want to move imports into a function if the
modules are only ever used in that function.  Note that loading a module the
first time may be expensive because of the one time initialization of the
module, but loading a module multiple times is virtually free, costing only a
couple of dictionary lookups.  Even if the module name has gone out of scope,
the module is probably available in :data:`sys.modules`.

If only instances of a specific class use a module, then it is reasonable to
import the module in the class's ``__init__`` method and then assign the module
to an instance variable so that the module is always available (via that
instance variable) during the life of the object.  Note that to delay an import
until the class is instantiated, the import must be inside a method.  Putting
the import inside the class but outside of any method still causes the import to
occur when the module is initialized.


How can I pass optional or keyword parameters from one function to another?
---------------------------------------------------------------------------

Collect the arguments using the ``*`` and ``**`` specifiers in the function's
parameter list; this gives you the positional arguments as a tuple and the
keyword arguments as a dictionary.  You can then pass these arguments when
calling another function by using ``*`` and ``**``::

   def f(x, *args, **kwargs):
       ...
       kwargs['width'] = '14.3c'
       ...
       g(x, *args, **kwargs)

In the unlikely case that you care about Python versions older than 2.0, use
:func:`apply`::

   def f(x, *args, **kwargs):
       ...
       kwargs['width'] = '14.3c'
       ...
       apply(g, (x,)+args, kwargs)


How do I write a function with output parameters (call by reference)?
---------------------------------------------------------------------

Remember that arguments are passed by assignment in Python.  Since assignment
just creates references to objects, there's no alias between an argument name in
the caller and callee, and so no call-by-reference per se.  You can achieve the
desired effect in a number of ways.

1) By returning a tuple of the results::

      def func2(a, b):
          a = 'new-value'        # a and b are local names
          b = b + 1              # assigned to new objects
          return a, b            # return new values

      x, y = 'old-value', 99
      x, y = func2(x, y)
      print x, y                 # output: new-value 100

   This is almost always the clearest solution.

2) By using global variables.  This isn't thread-safe, and is not recommended.

3) By passing a mutable (changeable in-place) object::

      def func1(a):
          a[0] = 'new-value'     # 'a' references a mutable list
          a[1] = a[1] + 1        # changes a shared object

      args = ['old-value', 99]
      func1(args)
      print args[0], args[1]     # output: new-value 100

4) By passing in a dictionary that gets mutated::

      def func3(args):
          args['a'] = 'new-value'     # args is a mutable dictionary
          args['b'] = args['b'] + 1   # change it in-place

      args = {'a':' old-value', 'b': 99}
      func3(args)
      print args['a'], args['b']

5) Or bundle up values in a class instance::

      class callByRef:
          def __init__(self, **args):
              for (key, value) in args.items():
                  setattr(self, key, value)

      def func4(args):
          args.a = 'new-value'        # args is a mutable callByRef
          args.b = args.b + 1         # change object in-place

      args = callByRef(a='old-value', b=99)
      func4(args)
      print args.a, args.b


   There's almost never a good reason to get this complicated.

Your best choice is to return a tuple containing the multiple results.


How do you make a higher order function in Python?
--------------------------------------------------

You have two choices: you can use nested scopes or you can use callable objects.
For example, suppose you wanted to define ``linear(a,b)`` which returns a
function ``f(x)`` that computes the value ``a*x+b``.  Using nested scopes::

   def linear(a, b):
       def result(x):
           return a * x + b
       return result

Or using a callable object::

   class linear:

       def __init__(self, a, b):
           self.a, self.b = a, b

       def __call__(self, x):
           return self.a * x + self.b

In both cases, ::

   taxes = linear(0.3, 2)

gives a callable object where ``taxes(10e6) == 0.3 * 10e6 + 2``.

The callable object approach has the disadvantage that it is a bit slower and
results in slightly longer code.  However, note that a collection of callables
can share their signature via inheritance::

   class exponential(linear):
       # __init__ inherited
       def __call__(self, x):
           return self.a * (x ** self.b)

Object can encapsulate state for several methods::

   class counter:

       value = 0

       def set(self, x):
           self.value = x

       def up(self):
           self.value = self.value + 1

       def down(self):
           self.value = self.value - 1

   count = counter()
   inc, dec, reset = count.up, count.down, count.set

Here ``inc()``, ``dec()`` and ``reset()`` act like functions which share the
same counting variable.


How do I copy an object in Python?
----------------------------------

In general, try :func:`copy.copy` or :func:`copy.deepcopy` for the general case.
Not all objects can be copied, but most can.

Some objects can be copied more easily.  Dictionaries have a :meth:`~dict.copy`
method::

   newdict = olddict.copy()

Sequences can be copied by slicing::

   new_l = l[:]


How can I find the methods or attributes of an object?
------------------------------------------------------

For an instance x of a user-defined class, ``dir(x)`` returns an alphabetized
list of the names containing the instance attributes and methods and attributes
defined by its class.


How can my code discover the name of an object?
-----------------------------------------------

Generally speaking, it can't, because objects don't really have names.
Essentially, assignment always binds a name to a value; The same is true of
``def`` and ``class`` statements, but in that case the value is a
callable. Consider the following code::

   class A:
       pass

   B = A

   a = B()
   b = a
   print b
   <__main__.A instance at 0x16D07CC>
   print a
   <__main__.A instance at 0x16D07CC>

Arguably the class has a name: even though it is bound to two names and invoked
through the name B the created instance is still reported as an instance of
class A.  However, it is impossible to say whether the instance's name is a or
b, since both names are bound to the same value.

Generally speaking it should not be necessary for your code to "know the names"
of particular values. Unless you are deliberately writing introspective
programs, this is usually an indication that a change of approach might be
beneficial.

In comp.lang.python, Fredrik Lundh once gave an excellent analogy in answer to
this question:

   The same way as you get the name of that cat you found on your porch: the cat
   (object) itself cannot tell you its name, and it doesn't really care -- so
   the only way to find out what it's called is to ask all your neighbours
   (namespaces) if it's their cat (object)...

   ....and don't be surprised if you'll find that it's known by many names, or
   no name at all!


What's up with the comma operator's precedence?
-----------------------------------------------

Comma is not an operator in Python.  Consider this session::

    >>> "a" in "b", "a"
    (False, 'a')

Since the comma is not an operator, but a separator between expressions the
above is evaluated as if you had entered::

    >>> ("a" in "b"), "a"

not::

    >>> "a" in ("b", "a")

The same is true of the various assignment operators (``=``, ``+=`` etc).  They
are not truly operators but syntactic delimiters in assignment statements.


Is there an equivalent of C's "?:" ternary operator?
----------------------------------------------------

Yes, this feature was added in Python 2.5. The syntax would be as follows::

   [on_true] if [expression] else [on_false]

   x, y = 50, 25

   small = x if x < y else y

For versions previous to 2.5 the answer would be 'No'.

.. XXX remove rest?

In many cases you can mimic ``a ? b : c`` with ``a and b or c``, but there's a
flaw: if *b* is zero (or empty, or ``None`` -- anything that tests false) then
*c* will be selected instead.  In many cases you can prove by looking at the
code that this can't happen (e.g. because *b* is a constant or has a type that
can never be false), but in general this can be a problem.

Tim Peters (who wishes it was Steve Majewski) suggested the following solution:
``(a and [b] or [c])[0]``.  Because ``[b]`` is a singleton list it is never
false, so the wrong path is never taken; then applying ``[0]`` to the whole
thing gets the *b* or *c* that you really wanted.  Ugly, but it gets you there
in the rare cases where it is really inconvenient to rewrite your code using
'if'.

The best course is usually to write a simple ``if...else`` statement.  Another
solution is to implement the ``?:`` operator as a function::

   def q(cond, on_true, on_false):
       if cond:
           if not isfunction(on_true):
               return on_true
           else:
               return on_true()
       else:
           if not isfunction(on_false):
               return on_false
           else:
               return on_false()

In most cases you'll pass b and c directly: ``q(a, b, c)``.  To avoid evaluating
b or c when they shouldn't be, encapsulate them within a lambda function, e.g.:
``q(a, lambda: b, lambda: c)``.

It has been asked *why* Python has no if-then-else expression.  There are
several answers: many languages do just fine without one; it can easily lead to
less readable code; no sufficiently "Pythonic" syntax has been discovered; a
search of the standard library found remarkably few places where using an
if-then-else expression would make the code more understandable.

In 2002, :pep:`308` was written proposing several possible syntaxes and the
community was asked to vote on the issue.  The vote was inconclusive.  Most
people liked one of the syntaxes, but also hated other syntaxes; many votes
implied that people preferred no ternary operator rather than having a syntax
they hated.


Is it possible to write obfuscated one-liners in Python?
--------------------------------------------------------

Yes.  Usually this is done by nesting :keyword:`lambda` within
:keyword:`lambda`.  See the following three examples, due to Ulf Bartelt::

   # Primes < 1000
   print filter(None,map(lambda y:y*reduce(lambda x,y:x*y!=0,
   map(lambda x,y=y:y%x,range(2,int(pow(y,0.5)+1))),1),range(2,1000)))

   # First 10 Fibonacci numbers
   print map(lambda x,f=lambda x,f:(f(x-1,f)+f(x-2,f)) if x>1 else 1: f(x,f),
   range(10))

   # Mandelbrot set
   print (lambda Ru,Ro,Iu,Io,IM,Sx,Sy:reduce(lambda x,y:x+y,map(lambda y,
   Iu=Iu,Io=Io,Ru=Ru,Ro=Ro,Sy=Sy,L=lambda yc,Iu=Iu,Io=Io,Ru=Ru,Ro=Ro,i=IM,
   Sx=Sx,Sy=Sy:reduce(lambda x,y:x+y,map(lambda x,xc=Ru,yc=yc,Ru=Ru,Ro=Ro,
   i=i,Sx=Sx,F=lambda xc,yc,x,y,k,f=lambda xc,yc,x,y,k,f:(k<=0)or (x*x+y*y
   >=4.0) or 1+f(xc,yc,x*x-y*y+xc,2.0*x*y+yc,k-1,f):f(xc,yc,x,y,k,f):chr(
   64+F(Ru+x*(Ro-Ru)/Sx,yc,0,0,i)),range(Sx))):L(Iu+y*(Io-Iu)/Sy),range(Sy
   ))))(-2.1, 0.7, -1.2, 1.2, 30, 80, 24)
   #    \___ ___/  \___ ___/  |   |   |__ lines on screen
   #        V          V      |   |______ columns on screen
   #        |          |      |__________ maximum of "iterations"
   #        |          |_________________ range on y axis
   #        |____________________________ range on x axis

Don't try this at home, kids!


Numbers and strings
===================

How do I specify hexadecimal and octal integers?
------------------------------------------------

To specify an octal digit, precede the octal value with a zero, and then a lower
or uppercase "o".  For example, to set the variable "a" to the octal value "10"
(8 in decimal), type::

   >>> a = 0o10
   >>> a
   8

Hexadecimal is just as easy.  Simply precede the hexadecimal number with a zero,
and then a lower or uppercase "x".  Hexadecimal digits can be specified in lower
or uppercase.  For example, in the Python interpreter::

   >>> a = 0xa5
   >>> a
   165
   >>> b = 0XB2
   >>> b
   178


Why does -22 // 10 return -3?
-----------------------------

It's primarily driven by the desire that ``i % j`` have the same sign as ``j``.
If you want that, and also want::

    i == (i // j) * j + (i % j)

then integer division has to return the floor.  C also requires that identity to
hold, and then compilers that truncate ``i // j`` need to make ``i % j`` have
the same sign as ``i``.

There are few real use cases for ``i % j`` when ``j`` is negative.  When ``j``
is positive, there are many, and in virtually all of them it's more useful for
``i % j`` to be ``>= 0``.  If the clock says 10 now, what did it say 200 hours
ago?  ``-190 % 12 == 2`` is useful; ``-190 % 12 == -10`` is a bug waiting to
bite.

.. note::

   On Python 2, ``a / b`` returns the same as ``a // b`` if
   ``__future__.division`` is not in effect.  This is also known as "classic"
   division.


How do I convert a string to a number?
--------------------------------------

For integers, use the built-in :func:`int` type constructor, e.g. ``int('144')
== 144``.  Similarly, :func:`float` converts to floating-point,
e.g. ``float('144') == 144.0``.

By default, these interpret the number as decimal, so that ``int('0144') ==
144`` and ``int('0x144')`` raises :exc:`ValueError`. ``int(string, base)`` takes
the base to convert from as a second optional argument, so ``int('0x144', 16) ==
324``.  If the base is specified as 0, the number is interpreted using Python's
rules: a leading '0' indicates octal, and '0x' indicates a hex number.

Do not use the built-in function :func:`eval` if all you need is to convert
strings to numbers.  :func:`eval` will be significantly slower and it presents a
security risk: someone could pass you a Python expression that might have
unwanted side effects.  For example, someone could pass
``__import__('os').system("rm -rf $HOME")`` which would erase your home
directory.

:func:`eval` also has the effect of interpreting numbers as Python expressions,
so that e.g. ``eval('09')`` gives a syntax error because Python regards numbers
starting with '0' as octal (base 8).


How do I convert a number to a string?
--------------------------------------

To convert, e.g., the number 144 to the string '144', use the built-in type
constructor :func:`str`.  If you want a hexadecimal or octal representation, use
the built-in functions :func:`hex` or :func:`oct`.  For fancy formatting, see
the :ref:`formatstrings` section, e.g. ``"{:04d}".format(144)`` yields
``'0144'`` and ``"{:.3f}".format(1/3)`` yields ``'0.333'``.  You may also use
:ref:`the % operator <string-formatting>` on strings.  See the library reference
manual for details.


How do I modify a string in place?
----------------------------------

You can't, because strings are immutable.  If you need an object with this
ability, try converting the string to a list or use the array module::

   >>> s = "Hello, world"
   >>> a = list(s)
   >>> print a
   ['H', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd']
   >>> a[7:] = list("there!")
   >>> ''.join(a)
   'Hello, there!'

   >>> import array
   >>> a = array.array('c', s)
   >>> print a
   array('c', 'Hello, world')
   >>> a[0] = 'y' ; print a
   array('c', 'yello world')
   >>> a.tostring()
   'yello, world'


How do I use strings to call functions/methods?
-----------------------------------------------

There are various techniques.

* The best is to use a dictionary that maps strings to functions.  The primary
  advantage of this technique is that the strings do not need to match the names
  of the functions.  This is also the primary technique used to emulate a case
  construct::

     def a():
         pass

     def b():
         pass

     dispatch = {'go': a, 'stop': b}  # Note lack of parens for funcs

     dispatch[get_input()]()  # Note trailing parens to call function

* Use the built-in function :func:`getattr`::

     import foo
     getattr(foo, 'bar')()

  Note that :func:`getattr` works on any object, including classes, class
  instances, modules, and so on.

  This is used in several places in the standard library, like this::

     class Foo:
         def do_foo(self):
             ...

         def do_bar(self):
             ...

     f = getattr(foo_instance, 'do_' + opname)
     f()


* Use :func:`locals` or :func:`eval` to resolve the function name::

     def myFunc():
         print "hello"

     fname = "myFunc"

     f = locals()[fname]
     f()

     f = eval(fname)
     f()

  Note: Using :func:`eval` is slow and dangerous.  If you don't have absolute
  control over the contents of the string, someone could pass a string that
  resulted in an arbitrary function being executed.

Is there an equivalent to Perl's chomp() for removing trailing newlines from strings?
-------------------------------------------------------------------------------------

Starting with Python 2.2, you can use ``S.rstrip("\r\n")`` to remove all
occurrences of any line terminator from the end of the string ``S`` without
removing other trailing whitespace.  If the string ``S`` represents more than
one line, with several empty lines at the end, the line terminators for all the
blank lines will be removed::

   >>> lines = ("line 1 \r\n"
   ...          "\r\n"
   ...          "\r\n")
   >>> lines.rstrip("\n\r")
   'line 1 '

Since this is typically only desired when reading text one line at a time, using
``S.rstrip()`` this way works well.

For older versions of Python, there are two partial substitutes:

- If you want to remove all trailing whitespace, use the ``rstrip()`` method of
  string objects.  This removes all trailing whitespace, not just a single
  newline.

- Otherwise, if there is only one line in the string ``S``, use
  ``S.splitlines()[0]``.


Is there a scanf() or sscanf() equivalent?
------------------------------------------

Not as such.

For simple input parsing, the easiest approach is usually to split the line into
whitespace-delimited words using the :meth:`~str.split` method of string objects
and then convert decimal strings to numeric values using :func:`int` or
:func:`float`.  ``split()`` supports an optional "sep" parameter which is useful
if the line uses something other than whitespace as a separator.

For more complicated input parsing, regular expressions are more powerful
than C's :cfunc:`sscanf` and better suited for the task.


What does 'UnicodeError: ASCII [decoding,encoding] error: ordinal not in range(128)' mean?
------------------------------------------------------------------------------------------

This error indicates that your Python installation can handle only 7-bit ASCII
strings.  There are a couple ways to fix or work around the problem.

If your programs must handle data in arbitrary character set encodings, the
environment the application runs in will generally identify the encoding of the
data it is handing you.  You need to convert the input to Unicode data using
that encoding.  For example, a program that handles email or web input will
typically find character set encoding information in Content-Type headers.  This
can then be used to properly convert input data to Unicode. Assuming the string
referred to by ``value`` is encoded as UTF-8::

   value = unicode(value, "utf-8")

will return a Unicode object.  If the data is not correctly encoded as UTF-8,
the above call will raise a :exc:`UnicodeError` exception.

If you only want strings converted to Unicode which have non-ASCII data, you can
try converting them first assuming an ASCII encoding, and then generate Unicode
objects if that fails::

   try:
       x = unicode(value, "ascii")
   except UnicodeError:
       value = unicode(value, "utf-8")
   else:
       # value was valid ASCII data
       pass

It's possible to set a default encoding in a file called ``sitecustomize.py``
that's part of the Python library.  However, this isn't recommended because
changing the Python-wide default encoding may cause third-party extension
modules to fail.

Note that on Windows, there is an encoding known as "mbcs", which uses an
encoding specific to your current locale.  In many cases, and particularly when
working with COM, this may be an appropriate default encoding to use.


Sequences (Tuples/Lists)
========================

How do I convert between tuples and lists?
------------------------------------------

The type constructor ``tuple(seq)`` converts any sequence (actually, any
iterable) into a tuple with the same items in the same order.

For example, ``tuple([1, 2, 3])`` yields ``(1, 2, 3)`` and ``tuple('abc')``
yields ``('a', 'b', 'c')``.  If the argument is a tuple, it does not make a copy
but returns the same object, so it is cheap to call :func:`tuple` when you
aren't sure that an object is already a tuple.

The type constructor ``list(seq)`` converts any sequence or iterable into a list
with the same items in the same order.  For example, ``list((1, 2, 3))`` yields
``[1, 2, 3]`` and ``list('abc')`` yields ``['a', 'b', 'c']``.  If the argument
is a list, it makes a copy just like ``seq[:]`` would.


What's a negative index?
------------------------

Python sequences are indexed with positive numbers and negative numbers.  For
positive numbers 0 is the first index 1 is the second index and so forth.  For
negative indices -1 is the last index and -2 is the penultimate (next to last)
index and so forth.  Think of ``seq[-n]`` as the same as ``seq[len(seq)-n]``.

Using negative indices can be very convenient.  For example ``S[:-1]`` is all of
the string except for its last character, which is useful for removing the
trailing newline from a string.


How do I iterate over a sequence in reverse order?
--------------------------------------------------

Use the :func:`reversed` built-in function, which is new in Python 2.4::

   for x in reversed(sequence):
       ... # do something with x...

This won't touch your original sequence, but build a new copy with reversed
order to iterate over.

With Python 2.3, you can use an extended slice syntax::

   for x in sequence[::-1]:
       ... # do something with x...


How do you remove duplicates from a list?
-----------------------------------------

See the Python Cookbook for a long discussion of many ways to do this:

    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52560

If you don't mind reordering the list, sort it and then scan from the end of the
list, deleting duplicates as you go::

   if mylist:
       mylist.sort()
       last = mylist[-1]
       for i in range(len(mylist)-2, -1, -1):
           if last == mylist[i]:
               del mylist[i]
           else:
               last = mylist[i]

If all elements of the list may be used as dictionary keys (i.e. they are all
hashable) this is often faster ::

   d = {}
   for x in mylist:
       d[x] = 1
   mylist = list(d.keys())

In Python 2.5 and later, the following is possible instead::

   mylist = list(set(mylist))

This converts the list into a set, thereby removing duplicates, and then back
into a list.


How do you make an array in Python?
-----------------------------------

Use a list::

   ["this", 1, "is", "an", "array"]

Lists are equivalent to C or Pascal arrays in their time complexity; the primary
difference is that a Python list can contain objects of many different types.

The ``array`` module also provides methods for creating arrays of fixed types
with compact representations, but they are slower to index than lists.  Also
note that the Numeric extensions and others define array-like structures with
various characteristics as well.

To get Lisp-style linked lists, you can emulate cons cells using tuples::

   lisp_list = ("like",  ("this",  ("example", None) ) )

If mutability is desired, you could use lists instead of tuples.  Here the
analogue of lisp car is ``lisp_list[0]`` and the analogue of cdr is
``lisp_list[1]``.  Only do this if you're sure you really need to, because it's
usually a lot slower than using Python lists.


How do I create a multidimensional list?
----------------------------------------

You probably tried to make a multidimensional array like this::

   A = [[None] * 2] * 3

This looks correct if you print it::

   >>> A
   [[None, None], [None, None], [None, None]]

But when you assign a value, it shows up in multiple places:

  >>> A[0][0] = 5
  >>> A
  [[5, None], [5, None], [5, None]]

The reason is that replicating a list with ``*`` doesn't create copies, it only
creates references to the existing objects.  The ``*3`` creates a list
containing 3 references to the same list of length two.  Changes to one row will
show in all rows, which is almost certainly not what you want.

The suggested approach is to create a list of the desired length first and then
fill in each element with a newly created list::

   A = [None] * 3
   for i in range(3):
       A[i] = [None] * 2

This generates a list containing 3 different lists of length two.  You can also
use a list comprehension::

   w, h = 2, 3
   A = [[None] * w for i in range(h)]

Or, you can use an extension that provides a matrix datatype; `Numeric Python
<http://numpy.scipy.org/>`_ is the best known.


How do I apply a method to a sequence of objects?
-------------------------------------------------

Use a list comprehension::

   result = [obj.method() for obj in mylist]

More generically, you can try the following function::

   def method_map(objects, method, arguments):
       """method_map([a,b], "meth", (1,2)) gives [a.meth(1,2), b.meth(1,2)]"""
       nobjects = len(objects)
       methods = map(getattr, objects, [method]*nobjects)
       return map(apply, methods, [arguments]*nobjects)


Dictionaries
============

How can I get a dictionary to display its keys in a consistent order?
---------------------------------------------------------------------

You can't.  Dictionaries store their keys in an unpredictable order, so the
display order of a dictionary's elements will be similarly unpredictable.

This can be frustrating if you want to save a printable version to a file, make
some changes and then compare it with some other printed dictionary.  In this
case, use the ``pprint`` module to pretty-print the dictionary; the items will
be presented in order sorted by the key.

A more complicated solution is to subclass ``dict`` to create a
``SortedDict`` class that prints itself in a predictable order.  Here's one
simpleminded implementation of such a class::

   class SortedDict(dict):
       def __repr__(self):
           keys = sorted(self.keys())
           result = ("{!r}: {!r}".format(k, self[k]) for k in keys)
           return "{{{}}}".format(", ".join(result))

       __str__ = __repr__

This will work for many common situations you might encounter, though it's far
from a perfect solution. The largest flaw is that if some values in the
dictionary are also dictionaries, their values won't be presented in any
particular order.


I want to do a complicated sort: can you do a Schwartzian Transform in Python?
------------------------------------------------------------------------------

The technique, attributed to Randal Schwartz of the Perl community, sorts the
elements of a list by a metric which maps each element to its "sort value". In
Python, just use the ``key`` argument for the ``sort()`` method::

   Isorted = L[:]
   Isorted.sort(key=lambda s: int(s[10:15]))

The ``key`` argument is new in Python 2.4, for older versions this kind of
sorting is quite simple to do with list comprehensions.  To sort a list of
strings by their uppercase values::

  tmp1 = [(x.upper(), x) for x in L]  # Schwartzian transform
  tmp1.sort()
  Usorted = [x[1] for x in tmp1]

To sort by the integer value of a subfield extending from positions 10-15 in
each string::

  tmp2 = [(int(s[10:15]), s) for s in L]  # Schwartzian transform
  tmp2.sort()
  Isorted = [x[1] for x in tmp2]

Note that Isorted may also be computed by ::

   def intfield(s):
       return int(s[10:15])

   def Icmp(s1, s2):
       return cmp(intfield(s1), intfield(s2))

   Isorted = L[:]
   Isorted.sort(Icmp)

but since this method calls ``intfield()`` many times for each element of L, it
is slower than the Schwartzian Transform.


How can I sort one list by values from another list?
----------------------------------------------------

Merge them into a single list of tuples, sort the resulting list, and then pick
out the element you want. ::

   >>> list1 = ["what", "I'm", "sorting", "by"]
   >>> list2 = ["something", "else", "to", "sort"]
   >>> pairs = zip(list1, list2)
   >>> pairs
   [('what', 'something'), ("I'm", 'else'), ('sorting', 'to'), ('by', 'sort')]
   >>> pairs.sort()
   >>> result = [ x[1] for x in pairs ]
   >>> result
   ['else', 'sort', 'to', 'something']

An alternative for the last step is::

   >>> result = []
   >>> for p in pairs: result.append(p[1])

If you find this more legible, you might prefer to use this instead of the final
list comprehension.  However, it is almost twice as slow for long lists.  Why?
First, the ``append()`` operation has to reallocate memory, and while it uses
some tricks to avoid doing that each time, it still has to do it occasionally,
and that costs quite a bit.  Second, the expression "result.append" requires an
extra attribute lookup, and third, there's a speed reduction from having to make
all those function calls.


Objects
=======

What is a class?
----------------

A class is the particular object type created by executing a class statement.
Class objects are used as templates to create instance objects, which embody
both the data (attributes) and code (methods) specific to a datatype.

A class can be based on one or more other classes, called its base class(es). It
then inherits the attributes and methods of its base classes. This allows an
object model to be successively refined by inheritance.  You might have a
generic ``Mailbox`` class that provides basic accessor methods for a mailbox,
and subclasses such as ``MboxMailbox``, ``MaildirMailbox``, ``OutlookMailbox``
that handle various specific mailbox formats.


What is a method?
-----------------

A method is a function on some object ``x`` that you normally call as
``x.name(arguments...)``.  Methods are defined as functions inside the class
definition::

   class C:
       def meth (self, arg):
           return arg * 2 + self.attribute


What is self?
-------------

Self is merely a conventional name for the first argument of a method.  A method
defined as ``meth(self, a, b, c)`` should be called as ``x.meth(a, b, c)`` for
some instance ``x`` of the class in which the definition occurs; the called
method will think it is called as ``meth(x, a, b, c)``.

See also :ref:`why-self`.


How do I check if an object is an instance of a given class or of a subclass of it?
-----------------------------------------------------------------------------------

Use the built-in function ``isinstance(obj, cls)``.  You can check if an object
is an instance of any of a number of classes by providing a tuple instead of a
single class, e.g. ``isinstance(obj, (class1, class2, ...))``, and can also
check whether an object is one of Python's built-in types, e.g.
``isinstance(obj, str)`` or ``isinstance(obj, (int, long, float, complex))``.

Note that most programs do not use :func:`isinstance` on user-defined classes
very often.  If you are developing the classes yourself, a more proper
object-oriented style is to define methods on the classes that encapsulate a
particular behaviour, instead of checking the object's class and doing a
different thing based on what class it is.  For example, if you have a function
that does something::

   def search(obj):
       if isinstance(obj, Mailbox):
           # ... code to search a mailbox
       elif isinstance(obj, Document):
           # ... code to search a document
       elif ...

A better approach is to define a ``search()`` method on all the classes and just
call it::

   class Mailbox:
       def search(self):
           # ... code to search a mailbox

   class Document:
       def search(self):
           # ... code to search a document

   obj.search()


What is delegation?
-------------------

Delegation is an object oriented technique (also called a design pattern).
Let's say you have an object ``x`` and want to change the behaviour of just one
of its methods.  You can create a new class that provides a new implementation
of the method you're interested in changing and delegates all other methods to
the corresponding method of ``x``.

Python programmers can easily implement delegation.  For example, the following
class implements a class that behaves like a file but converts all written data
to uppercase::

   class UpperOut:

       def __init__(self, outfile):
           self._outfile = outfile

       def write(self, s):
           self._outfile.write(s.upper())

       def __getattr__(self, name):
           return getattr(self._outfile, name)

Here the ``UpperOut`` class redefines the ``write()`` method to convert the
argument string to uppercase before calling the underlying
``self.__outfile.write()`` method.  All other methods are delegated to the
underlying ``self.__outfile`` object.  The delegation is accomplished via the
``__getattr__`` method; consult :ref:`the language reference <attribute-access>`
for more information about controlling attribute access.

Note that for more general cases delegation can get trickier. When attributes
must be set as well as retrieved, the class must define a :meth:`__setattr__`
method too, and it must do so carefully.  The basic implementation of
:meth:`__setattr__` is roughly equivalent to the following::

   class X:
       ...
       def __setattr__(self, name, value):
           self.__dict__[name] = value
       ...

Most :meth:`__setattr__` implementations must modify ``self.__dict__`` to store
local state for self without causing an infinite recursion.


How do I call a method defined in a base class from a derived class that overrides it?
--------------------------------------------------------------------------------------

If you're using new-style classes, use the built-in :func:`super` function::

   class Derived(Base):
       def meth (self):
           super(Derived, self).meth()

If you're using classic classes: For a class definition such as ``class
Derived(Base): ...`` you can call method ``meth()`` defined in ``Base`` (or one
of ``Base``'s base classes) as ``Base.meth(self, arguments...)``.  Here,
``Base.meth`` is an unbound method, so you need to provide the ``self``
argument.


How can I organize my code to make it easier to change the base class?
----------------------------------------------------------------------

You could define an alias for the base class, assign the real base class to it
before your class definition, and use the alias throughout your class.  Then all
you have to change is the value assigned to the alias.  Incidentally, this trick
is also handy if you want to decide dynamically (e.g. depending on availability
of resources) which base class to use.  Example::

   BaseAlias = <real base class>

   class Derived(BaseAlias):
       def meth(self):
           BaseAlias.meth(self)
           ...


How do I create static class data and static class methods?
-----------------------------------------------------------

Both static data and static methods (in the sense of C++ or Java) are supported
in Python.

For static data, simply define a class attribute.  To assign a new value to the
attribute, you have to explicitly use the class name in the assignment::

   class C:
       count = 0   # number of times C.__init__ called

       def __init__(self):
           C.count = C.count + 1

       def getcount(self):
           return C.count  # or return self.count

``c.count`` also refers to ``C.count`` for any ``c`` such that ``isinstance(c,
C)`` holds, unless overridden by ``c`` itself or by some class on the base-class
search path from ``c.__class__`` back to ``C``.

Caution: within a method of C, an assignment like ``self.count = 42`` creates a
new and unrelated instance named "count" in ``self``'s own dict.  Rebinding of a
class-static data name must always specify the class whether inside a method or
not::

   C.count = 314

Static methods are possible since Python 2.2::

   class C:
       def static(arg1, arg2, arg3):
           # No 'self' parameter!
           ...
       static = staticmethod(static)

With Python 2.4's decorators, this can also be written as ::

   class C:
       @staticmethod
       def static(arg1, arg2, arg3):
           # No 'self' parameter!
           ...

However, a far more straightforward way to get the effect of a static method is
via a simple module-level function::

   def getcount():
       return C.count

If your code is structured so as to define one class (or tightly related class
hierarchy) per module, this supplies the desired encapsulation.


How can I overload constructors (or methods) in Python?
-------------------------------------------------------

This answer actually applies to all methods, but the question usually comes up
first in the context of constructors.

In C++ you'd write

.. code-block:: c

    class C {
        C() { cout << "No arguments\n"; }
        C(int i) { cout << "Argument is " << i << "\n"; }
    }

In Python you have to write a single constructor that catches all cases using
default arguments.  For example::

   class C:
       def __init__(self, i=None):
           if i is None:
               print "No arguments"
           else:
               print "Argument is", i

This is not entirely equivalent, but close enough in practice.

You could also try a variable-length argument list, e.g. ::

   def __init__(self, *args):
       ...

The same approach works for all method definitions.


I try to use __spam and I get an error about _SomeClassName__spam.
------------------------------------------------------------------

Variable names with double leading underscores are "mangled" to provide a simple
but effective way to define class private variables.  Any identifier of the form
``__spam`` (at least two leading underscores, at most one trailing underscore)
is textually replaced with ``_classname__spam``, where ``classname`` is the
current class name with any leading underscores stripped.

This doesn't guarantee privacy: an outside user can still deliberately access
the "_classname__spam" attribute, and private values are visible in the object's
``__dict__``.  Many Python programmers never bother to use private variable
names at all.


My class defines __del__ but it is not called when I delete the object.
-----------------------------------------------------------------------

There are several possible reasons for this.

The del statement does not necessarily call :meth:`__del__` -- it simply
decrements the object's reference count, and if this reaches zero
:meth:`__del__` is called.

If your data structures contain circular links (e.g. a tree where each child has
a parent reference and each parent has a list of children) the reference counts
will never go back to zero.  Once in a while Python runs an algorithm to detect
such cycles, but the garbage collector might run some time after the last
reference to your data structure vanishes, so your :meth:`__del__` method may be
called at an inconvenient and random time. This is inconvenient if you're trying
to reproduce a problem. Worse, the order in which object's :meth:`__del__`
methods are executed is arbitrary.  You can run :func:`gc.collect` to force a
collection, but there *are* pathological cases where objects will never be
collected.

Despite the cycle collector, it's still a good idea to define an explicit
``close()`` method on objects to be called whenever you're done with them.  The
``close()`` method can then remove attributes that refer to subobjecs.  Don't
call :meth:`__del__` directly -- :meth:`__del__` should call ``close()`` and
``close()`` should make sure that it can be called more than once for the same
object.

Another way to avoid cyclical references is to use the :mod:`weakref` module,
which allows you to point to objects without incrementing their reference count.
Tree data structures, for instance, should use weak references for their parent
and sibling references (if they need them!).

If the object has ever been a local variable in a function that caught an
expression in an except clause, chances are that a reference to the object still
exists in that function's stack frame as contained in the stack trace.
Normally, calling :func:`sys.exc_clear` will take care of this by clearing the
last recorded exception.

Finally, if your :meth:`__del__` method raises an exception, a warning message
is printed to :data:`sys.stderr`.


How do I get a list of all instances of a given class?
------------------------------------------------------

Python does not keep track of all instances of a class (or of a built-in type).
You can program the class's constructor to keep track of all instances by
keeping a list of weak references to each instance.


Modules
=======

How do I create a .pyc file?
----------------------------

When a module is imported for the first time (or when the source is more recent
than the current compiled file) a ``.pyc`` file containing the compiled code
should be created in the same directory as the ``.py`` file.

One reason that a ``.pyc`` file may not be created is permissions problems with
the directory. This can happen, for example, if you develop as one user but run
as another, such as if you are testing with a web server.  Creation of a .pyc
file is automatic if you're importing a module and Python has the ability
(permissions, free space, etc...) to write the compiled module back to the
directory.

Running Python on a top level script is not considered an import and no ``.pyc``
will be created.  For example, if you have a top-level module ``abc.py`` that
imports another module ``xyz.py``, when you run abc, ``xyz.pyc`` will be created
since xyz is imported, but no ``abc.pyc`` file will be created since ``abc.py``
isn't being imported.

If you need to create abc.pyc -- that is, to create a .pyc file for a module
that is not imported -- you can, using the :mod:`py_compile` and
:mod:`compileall` modules.

The :mod:`py_compile` module can manually compile any module.  One way is to use
the ``compile()`` function in that module interactively::

   >>> import py_compile
   >>> py_compile.compile('abc.py')

This will write the ``.pyc`` to the same location as ``abc.py`` (or you can
override that with the optional parameter ``cfile``).

You can also automatically compile all files in a directory or directories using
the :mod:`compileall` module.  You can do it from the shell prompt by running
``compileall.py`` and providing the path of a directory containing Python files
to compile::

       python -m compileall .


How do I find the current module name?
--------------------------------------

A module can find out its own module name by looking at the predefined global
variable ``__name__``.  If this has the value ``'__main__'``, the program is
running as a script.  Many modules that are usually used by importing them also
provide a command-line interface or a self-test, and only execute this code
after checking ``__name__``::

   def main():
       print 'Running test...'
       ...

   if __name__ == '__main__':
       main()


How can I have modules that mutually import each other?
-------------------------------------------------------

Suppose you have the following modules:

foo.py::

   from bar import bar_var
   foo_var = 1

bar.py::

   from foo import foo_var
   bar_var = 2

The problem is that the interpreter will perform the following steps:

* main imports foo
* Empty globals for foo are created
* foo is compiled and starts executing
* foo imports bar
* Empty globals for bar are created
* bar is compiled and starts executing
* bar imports foo (which is a no-op since there already is a module named foo)
* bar.foo_var = foo.foo_var

The last step fails, because Python isn't done with interpreting ``foo`` yet and
the global symbol dictionary for ``foo`` is still empty.

The same thing happens when you use ``import foo``, and then try to access
``foo.foo_var`` in global code.

There are (at least) three possible workarounds for this problem.

Guido van Rossum recommends avoiding all uses of ``from <module> import ...``,
and placing all code inside functions.  Initializations of global variables and
class variables should use constants or built-in functions only.  This means
everything from an imported module is referenced as ``<module>.<name>``.

Jim Roskind suggests performing steps in the following order in each module:

* exports (globals, functions, and classes that don't need imported base
  classes)
* ``import`` statements
* active code (including globals that are initialized from imported values).

van Rossum doesn't like this approach much because the imports appear in a
strange place, but it does work.

Matthias Urlichs recommends restructuring your code so that the recursive import
is not necessary in the first place.

These solutions are not mutually exclusive.


__import__('x.y.z') returns <module 'x'>; how do I get z?
---------------------------------------------------------

Try::

   __import__('x.y.z').y.z

For more realistic situations, you may have to do something like ::

   m = __import__(s)
   for i in s.split(".")[1:]:
       m = getattr(m, i)

See :mod:`importlib` for a convenience function called
:func:`~importlib.import_module`.



When I edit an imported module and reimport it, the changes don't show up.  Why does this happen?
-------------------------------------------------------------------------------------------------

For reasons of efficiency as well as consistency, Python only reads the module
file on the first time a module is imported.  If it didn't, in a program
consisting of many modules where each one imports the same basic module, the
basic module would be parsed and re-parsed many times.  To force rereading of a
changed module, do this::

   import modname
   reload(modname)

Warning: this technique is not 100% fool-proof.  In particular, modules
containing statements like ::

   from modname import some_objects

will continue to work with the old version of the imported objects.  If the
module contains class definitions, existing class instances will *not* be
updated to use the new class definition.  This can result in the following
paradoxical behaviour:

   >>> import cls
   >>> c = cls.C()                # Create an instance of C
   >>> reload(cls)
   <module 'cls' from 'cls.pyc'>
   >>> isinstance(c, cls.C)       # isinstance is false?!?
   False

The nature of the problem is made clear if you print out the class objects:

   >>> c.__class__
   <class cls.C at 0x7352a0>
   >>> cls.C
   <class cls.C at 0x4198d0>

