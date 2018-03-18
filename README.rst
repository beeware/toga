.. image:: http://pybee.org/project/projects/libraries/toga/toga.png
    :width: 72px
    :target: https://pybee.org/toga

Toga
====

.. image:: https://img.shields.io/pypi/pyversions/toga.svg
    :target: https://pypi.python.org/pypi/toga

.. image:: https://img.shields.io/pypi/v/toga.svg
    :target: https://pypi.python.org/pypi/toga

.. image:: https://img.shields.io/pypi/status/toga.svg
    :target: https://pypi.python.org/pypi/toga

.. image:: https://img.shields.io/pypi/l/toga.svg
    :target: https://github.com/pybee/toga/blob/master/LICENSE

.. image:: https://beekeeper.herokuapp.com/projects/pybee/batavia/shield
    :target: https://beekeeper.herokuapp.com/projects/pybee/batavia

.. image:: https://badges.gitter.im/pybee/general.svg
    :target: https://gitter.im/pybee/general


A Python native, OS native GUI toolkit.

Prerequisites
~~~~~~~~~~~~~

Minimum requirements
^^^^^^^^^^^^^^^^^^^^

* Toga requires **Python 3**. Python 2 is not supported.

* If you're on macOS, you need to be on 10.7 (Lion) or newer.

* If you're on Linux, you need to have GTK+ 3.10 or later. This is the version
  that ships starting with Ubuntu 14.04 and Fedora 20. You also need to install
  the Python 3 bindings to GTK+.

* We're working on Windows support, but not all features and widgets are
  supported. At a minimum, you'll need Python 3 and .NET Framework 4. This has
  been tested on Windows 10, but should work on 7 and 8. Pull requests, help and
  corrections are most welcome.

Optional extras for Linux
^^^^^^^^^^^^^^^^^^^^^^^^^

In Linux, extra packages are needed if you want to:
1. Use the WebView widget
2. Use Toga inside a `Virtual Environment`_

* **Ubuntu / Debian** ``sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0 libgirepository1.0-dev``
  Note: for Ubuntu 14.04 install ``gir1.2-webkit-3.0`` instead of ``gir1.2-webkit-4.0``

* **Fedora** ``sudo dnf install pygobject3 python3-gobject pywebkitgtk python3-cairo-devel cairo-gobject-devel gobject-introspection-devel``
  or ``sudo yum install pygobject3 python3-gobject pywebkitgtk python3-cairo-devel cairo-gobject-devel gobject-introspection-devel``

* **Arch Linux** ``sudo pacman -S python-gobject webkit2gtk gobject-introspection``

Other distros should be similar, but feel free to send a pull request with
updated dependencies if needed.

If you are going to use Toga inside a `Virtual Environment`_, you need to
install pycairo and pygobject (in that order) in the virtualenv first::

    $ pip install pycairo
    $ pip install pygobject

If these requirements aren't met, Toga either won't work at all, or won't have
full functionality.

Quickstart
~~~~~~~~~~

To get a demonstration of the capabilities of Toga, run the following::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window with some sample widgets.

Documentation
~~~~~~~~~~~~~

Documentation for Toga can be found on `Read The Docs`_.

Community
~~~~~~~~~

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `pybee/general`_ channel on Gitter.

Contributing
~~~~~~~~~~~~

If you'd like to contribute to Toga development, our `guide for first time
contributors`_ will help you get started.

If you experience problems with Toga, `log them on GitHub`_. If you want to
contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: https://toga.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _pybee/general: https://gitter.im/pybee/general
.. _guide for first time contributors: https://toga.readthedocs.io/en/latest/how-to/contribute.html 
.. _log them on Github: https://github.com/pybee/toga/issues
.. _fork the code: https://github.com/pybee/toga
.. _submit a pull request: https://github.com/pybee/toga/pulls
.. _Virtual Environment: https://www.virtualenv.org
