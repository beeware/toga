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

    $ pip install -e .
    $ pip install -r requirements_dev.txt

Now you are ready to start hacking! Have fun!
