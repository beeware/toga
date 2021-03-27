.. image:: https://beeware.org/project/projects/libraries/toga/toga.png
    :width: 72px
    :target: https://beeware.org/toga

Toga
====

.. image:: https://img.shields.io/badge/python-3.5%2C%203.6%2C%203.7-blue.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Python Versions

.. image:: https://img.shields.io/pypi/v/toga.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Project version

.. image:: https://img.shields.io/pypi/status/toga.svg
    :target: https://pypi.python.org/pypi/toga
    :alt: Project status

.. image:: https://img.shields.io/pypi/l/toga.svg
    :target: https://github.com/beeware/toga/blob/master/LICENSE
    :alt: License

.. image:: https://github.com/beeware/toga/workflows/CI/badge.svg?branch=master
   :target: https://github.com/beeware/toga/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/beeware/toga/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/beeware/toga
   :alt: Codecov

.. image:: https://badges.gitter.im/beeware/general.svg
   :target: https://gitter.im/beeware/general
   :alt: Gitter chat room

A Python native, OS native GUI toolkit.

Prerequisites
~~~~~~~~~~~~~

Minimum requirements
^^^^^^^^^^^^^^^^^^^^

* Toga requires **Python 3**. Python 2 is not supported.

* If you're on macOS, you need to be on 10.10 (Yosemite) or newer.

* If you're on Linux, you need to have GTK+ 3.10 or later. This is the version
  that ships starting with Ubuntu 14.04 and Fedora 20. You also need to install
  the Python 3 bindings and development files for GTK+.

  * **Ubuntu 16.04 / Debian 9** ``sudo apt-get install python3-dev python3-gi python3-gi-cairo libgirepository1.0-dev libcairo2-dev libwebkitgtk-3.0-0 gir1.2-webkit2-3.0``

  * **Ubuntu 18.04 / Debian 10** ``sudo apt-get install python3-dev python3-gi python3-gi-cairo libgirepository1.0-dev libcairo2-dev libwebkitgtk-4.0-37 gir1.2-webkit2-4.0``

  * **Fedora** ``sudo dnf install pygobject3 python3-gobject python3-cairo-devel cairo-gobject-devel gobject-introspection-devel pywebkitgtk``

  * **Arch / Manjaro** ``sudo pacman -Syu git pkgconf cairo python-cairo pango gobject-introspection gobject-introspection-runtime python-gobject webkit2gtk``

* We're working on Windows support, but not all features and widgets are
  supported. At a minimum, you'll need Python 3 and .NET Framework 4. This has
  been tested on Windows 10, but should work on 7 and 8. Pull requests, help and
  corrections are most welcome.

Quickstart
~~~~~~~~~~

To get a demonstration of the capabilities of Toga, run the following::

    $ pip install --pre toga-demo
    $ toga-demo

This will pop up a GUI window with some sample widgets.

Documentation
~~~~~~~~~~~~~

Documentation for Toga can be found on `Read The Docs`_.

Community
~~~~~~~~~

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `beeware/general`_ channel on Gitter.

Contributing
~~~~~~~~~~~~

If you'd like to contribute to Toga development, our `guide for first time
contributors`_ will help you get started.

If you experience problems with Toga, `log them on GitHub`_. If you want to
contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: https://beeware.org/
.. _Read The Docs: https://toga.readthedocs.io
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _beeware/general: https://gitter.im/beeware/general
.. _guide for first time contributors: https://toga.readthedocs.io/en/latest/how-to/contribute.html
.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls
.. _Virtual Environment: https://www.virtualenv.org
