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

Toga uses ``unittest`` (or ``unittest2`` for Python < 2.7) for its own test
suite as well as additional helper modules for testing. To install all the
requirements for Toga, you have to run the following commands within your
virutal envrionment::

    $ pip install -e .
    $ pip install -r requirements_dev.txt

In case you are running a python version ``< 2.7`` please use the
``requirements_dev.py26.txt`` instead because ``unittest2`` is not part
of the standard library for these version.

Now you are ready to start hacking! Have fun!