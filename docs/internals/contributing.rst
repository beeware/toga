Contributing to Toga
====================


If you experience problems with Toga, `log them on GitHub`_. If you want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/pybee/toga/issues
.. _fork the code: https://github.com/pybee/toga
.. _submit a pull request: https://github.com/pybee/toga/pulls


Setting up your development environment
---------------------------------------

The recommended way of setting up your development envrionment for Toga
is to install a virtual environment, install the required dependencies and
start coding. Assuming that you are using ``virtualenvwrapper``, you only have
to run::

    $ git clone git@github.com:pybee/toga.git
    $ cd toga
    $ mkvirtualenv toga

.. note::

   Toga doesn't have a test suite yet. The high level plan is two add
   two types of tests to the project:

   1. Tests verifying that the core of Toga (contained in ``src/core/``
      -- the abstract widgets -- actually do what they are supposed to
      do.

   2. Tests for each backend.

..
   Toga uses ``unittest`` for its own test suite as well as additional
   helper modules for testing. To install all the requirements for Toga,
   you have to run the following commands within your virtual environment::

To get started, run the following commands within your virtual
environment (ensure that you're using Python 3.4 or better)::

    $ pip install -e src/core -e .

The somewhat odd command is required because the main Toga package is a
sort of "metapackage" which pulls other parts in; if you just do::

    $ pip install -e .  # Don't do this on its own

it will install the dependencies -- like ``toga_core`` -- from released versions
into your site packages, instead of using the sources.

Now you are ready to start hacking on the core of toga!

Of course, if you want to work on any specific platform, you need to do the
same for it::

    $ pip install -e src/core -e src/gtk -e .

Have fun!
