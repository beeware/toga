.. _contribute:

=========================
How to contribute to Toga
=========================

If you experience problems with Toga, `log them on GitHub`_. If you want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/pybee/toga/issues
.. _fork the code: https://github.com/pybee/toga
.. _submit a pull request: https://github.com/pybee/toga/pulls


Set up your development environment
===================================

The recommended way of setting up your development environment for Toga
is to install a virtual environment, install the required dependencies and
start coding. To set up a virtual environment, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Linux

    .. code-block:: bash

      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>python3 -m venv venv
      C:\...>venv/Scripts/activate

Your prompt should now have a ``(venv)`` prefix in front of it.

Next, go to `the Toga page on Github <https://github.com/pybee/toga>`__, and
fork the repository into your own account, and then clone a copy of that
repository onto your computer by clicking on "Clone or Download". If you
have the Github desktop application installed on your computer, you can
select "Open in Desktop"; otherwise, copy the URL provided, and use it
to clone using the command line:

.. tabs::

  .. group-tab:: macOS

    Fork the Toga repository, and then::

      (venv) $ git clone https://github.com/<your username>/toga.git

    (substituting your Github username)

  .. group-tab:: Linux

    Fork the Toga repository, and then::

      (venv) $ git clone https://github.com/<your username>/toga.git

    (substituting your Github username)

  .. group-tab:: Windows

    Fork the Toga repository, and then:

    .. code-block:: doscon

      (venv) C:\...>git clone https://github.com/<your username>/toga.git

    (substituting your Github username)

Now that you have the source code, you can install Toga into your development
environment. The Toga source repository contains multiple packages. Since
we're installing from source, we can't rely on pip to install the packages in
dependency order. Therefore, we have to manually install each package in a
specific order. We start with the core packages:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ cd toga
      (venv) $ pip install -e src/core
      (venv) $ pip install -e src/dummy

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ cd toga
      (venv) $ pip install -e src/core
      (venv) $ pip install -e src/dummy

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>cd toga
      (venv) C:\...>pip install -e src/core
      (venv) C:\...>pip install -e src/dummy

Then, we can install the code for the specific platform we want to use:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ pip install -e src/cocoa

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ pip install -e src/gtk

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>pip install -e src/winforms

You can then run the core test suite:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ cd src/core
      (venv) $ python setup.py test
      ...
      ----------------------------------------------------------------------
      Ran 181 tests in 0.343s

      OK (skipped=1)

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ cd src/core
      (venv) $ python setup.py test
      ...
      ----------------------------------------------------------------------
      Ran 181 tests in 0.343s

      OK (skipped=1)

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>cd src/core
      (venv) C:\...>python setup.py test
      ...
      ----------------------------------------------------------------------
      Ran 181 tests in 0.343s

      OK (skipped=1)

You should get some output indicating that tests have been run. You shouldn’t
ever get any FAIL or ERROR test results. We run our full test suite before
merging every patch. If that process discovers any problems, we don’t merge
the patch. If you do find a test error or failure, either there’s something
odd in your test environment, or you’ve found an edge case that we haven’t
seen before - either way, let us know!

Now you are ready to start hacking on Toga!

What should I do?
=================

The src/core package of toga has a test suite, but that test suite is
incomplete. There are many aspects of the Toga Core API that aren't currently
tested (or aren't tested thoroughly). To work out what *isn't* tested, we're
going to use a tool called `coverage
<http://coverage.readthedocs.io/en/coverage-4.4.1/>`__. Coverage allows you to
check which lines of code have (and haven't) been executed - which then gives
you an idea of what code has (and hasn't) been tested.

Install coverage, and then re-run the test suite -- this time, in a slightly
different way so that we can gather some data about the test run. Then we can
ask coverage to generate a report of the data that was gathered:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ pip install coverage
      (venv) $ coverage run setup.py test
      (venv) $ coverage report -m --include="toga/*"
      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     18    77%   58, 75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    258    75%

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ pip install coverage
      (venv) $ coverage run setup.py test
      (venv) $ coverage report -m --include="toga/*"
      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     18    77%   58, 75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    258    75%

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>pip install coverage
      (venv) C:\...>coverage run setup.py test
      (venv) C:\...>coverage report -m --include=toga/*
      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     18    77%   58, 75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    258    75%

What does this all mean? Well, the "Cover" column tells you what proportion of
lines in a given file were executed during the test run. In this run, every
line of ``toga/app.py`` was executed; but only 77% of lines in
``toga/window.py`` were executed. Which lines were missed? They're listed in
the next column: lines 58, 75, 87, and so on weren't executed.

That's what you have to fix - ideally, every single line in every single file
will have 100% coverage. If you look in `src/core/tests`, you should find a
test file that matches the name of the file that has insufficient coverage. If
you don't, it's possible the entire test file is missing - so you'll have to
create it!

Your task: create a test that improves coverage - even by one more line.

Once you've written a test, re-run the test suite to generate fresh coverage
data. Let's say we added a test for line 58 of ``toga/window.py`` - we'd
expect to see something like:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ coverage run setup.py test
      running test
      ...
      ----------------------------------------------------------------------
      Ran 101 tests in 0.343s

      OK (skipped=1)
      (venv) $ coverage report -m --include="toga/*"
      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     17    78%   75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    257    75%

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ coverage run setup.py test
      running test
      ...
      ----------------------------------------------------------------------
      Ran 101 tests in 0.343s

      OK (skipped=1)
      (venv) $ coverage report -m --include="toga/*"
      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     17    78%   75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    257    75%

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>coverage run setup.py test
      running test
      ...
      ----------------------------------------------------------------------
      Ran 101 tests in 0.343s

      OK (skipped=1)
      (venv) $ coverage report -m --include=toga/*
      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     17    78%   75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    257    75%


That is, one more test has been executed, resulting in one less missing line
in the coverage results.

Submit a pull request for your work, and you're done! Congratulations, you're
a contributor to Toga!

How does this all work?
=======================

Since you're writing tests for a GUI toolkit, you might be wondering why you
haven't seen a GUI yet. The Toga Core package contains the API definitions for
the Toga widget kit. This is completely platform agnostic - it just provides
an interface, and defers actually drawing anything on the screen to the
platform backends.

When you run the test suite, the test runner uses a "dummy" backend - a
platform backend that *implements* the full API, but doesn’t actually *do*
anything (i.e., when you say display a button, it creates an object, but
doesn’t actually display a button).

In this way, it's possible to for the Toga Core tests to exercise every API
entry point in the Toga Core package, verify that data is stored correctly on
the interface layer, and sent through to the right endpoints in the Dummy
backend. If the *dummy* backend is invoked correcty, then any other backend
will be handled correctly, too.

One error you might see...
--------------------------

When you're running these tests - especially when you submit your PR, and the
tests run on our continous integration (CI) server - it's possible you might get
and error that reads::

    ModuleNotFoundError: No module named 'toga_gtk'.

If this happens, you've found an bug in the way the widget you're testing
has been constructed.

The Core API is designed to be platform independent. When a widget is created,
it calls upon a "factory" to instantiate the underlying platform-dependent
implementation. When a Toga application starts running, it will try to guess
the right factory to use based on the environment where the code is running.
So, if you run your code on a Mac, it will use the Cocoa factory; if you're on
a Linux box, it will use the GTK factory.

However, when writing tests, we want to use the "dummy" factory. The Dummy
factory isn't the "native" platform anywhere - it's just a placeholder. As a
result, the  dummy factory won't be used unless you specifically request it -
which means every widget has to honor that request.

Most Toga widgets create their platform-specific implementation when they are
created. As a result, most Toga widgets should accept a ``factory`` argument -
and that factory should be used to instantiate any widget implementations or
sub-widgets.

However, *some* widgets - like Icon - are "late loaded" - the implmementation
isn't created until the widget is actually *used*. Late loaded widgets don't
accept a ``factory`` when they're created - but they *do* have an `_impl()`
method that accepts a factory.

If these factory arguments aren't being passed around correctly, then a test
suite will attempt to create a widget, but will fall back to the platform-
default factory, rather than the "dummy" factory. If you've installed the
appropriate platform default backend, you won't (necessarily) get an error,
but your tests won't use the dummy backend. On our CI server, we deliberately
don't install a platform backend so we can find these errors.

If you get the ``ModuleNotFoundError``, you need to audit the code to find out
where a widget is being created without a factory being specified.

It's not just about coverage!
=============================

Although improving test coverage is the goal, the task ahead of you isn't
*just* about increasing numerical coverage. Part of the task is to audit the
code as you go. You could write a comprehensive set of tests for a concrete
life jacket... but a concrete life jacket would still be useless for the
purpose it was intended!

As you develop tests and improve coverage, you should be checking that the
core module is internally **consistent** as well. If you notice any method
names that aren’t internally consistent (e.g., something called ``on_select``
in one module, but called ``on_selected`` in another), or where the data isn’t
being handled consistently (one widget updates then refreshes, but another
widget refreshes then updates), flag it and bring it to our attention by
raising a ticket. Or, if you're confident that you know what needs to be done,
create a pull request that fixes the problem you've found.

On example of the type of consistency we're looking for is described in
`this ticket <https://github.com/pybee/toga/issues/299>`__.

What next?
==========

Rinse and repeat! Having improved coverage by one line, go back and do it
again for *another* coverage line!

If you're feeling particularly adventurous, you could start looking at a
specific platform backend. The Toga Dummy API defines the API that a backend
needs to implement; so find a platform backend of interest to you (e.g., cocoa
if you're on macOS), and look for a widget that isn't implemented (a missing
file in the ``widgets`` directory for that platform, or an API *on* a widget
that isn't implemented (these will be flagged by raising
``NotImplementedError()``). Dig into the documentation for native widgets for
that platform (e.g., the Apple Cocoa documentation), and work out how to map
native widget capabilities to the Toga API. You may find it helpful to look at
existing widgets to work out what is needed.

Most importantly - have fun!

Advanced Mode
=============

If you've got expertise in a particular platform (for example, if you've got
experience writing iOS apps), or you'd *like* to have that experience, you
might want to look into a more advanced problem. Here are some suggestions:

* **Implement a platform native widget** If the core library already specifies
  an interface, implement that interface; if no interface exists, propose an
  interface design, and implement it for at least one platform.

* **Add a new feature to an existing widget API** Can you think of a feature
  than an existing widget should have? Propose a new API for that widget, and
  provide a sample implementation.

* **Improve platform specific testing** The tests that have been described in
  this document are all platform independent. They use the dummy backend to
  validate that data is being passed around correctly, but they don't validate
  that on a given platform, widgets behave they way they should. If I put a
  button on Toga app, is that button displayed? Is it in the right place? Does
  it respond to mouse clicks? Ideally, we'd have automated tests to validate
  these properties. However, automated tests of GUI operations can be difficult
  to set up. If you've got experience with automated GUI testing, we'd love to
  hear your suggestions.

* **Improve the testing API for application writers** The dummy backend exists
  to validate that Toga's internal API works as expected. However, we would like
  it to be a useful resource for *application* authors as well. Testing GUI
  applications is a difficult task; a Dummy backend would potentially allow an
  end user to write an application, and validate behavior by testing the
  properties of the Dummy. Think of it as a GUI mock - but one that is baked into
  Toga as a framework. See if you can write a GUI app of your own, and write
  a test suite that uses the Dummy backend to validate the behavior of that app.
