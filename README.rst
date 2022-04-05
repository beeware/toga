.. image:: https://beeware.org/project/projects/libraries/toga/toga.png
    :width: 72px
    :target: https://beeware.org/toga

Toga
====

.. image:: https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue.svg
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

.. image:: https://img.shields.io/discord/836455665257021440?label=Discord%20Chat&logo=discord&style=plastic
   :target: https://beeware.org/bee/chat/
   :alt: Discord server

A Python native, OS native GUI toolkit.

Prerequisites
~~~~~~~~~~~~~

Minimum requirements
^^^^^^^^^^^^^^^^^^^^

* Toga requires **Python 3.7 or higher**. Python 2 is not supported.

* If you're on macOS, you need to be on 10.10 (Yosemite) or newer.

* If you're on Linux, you need to have GTK+ 3.10 or newer. This is the version
  that ships starting with Ubuntu 14.04 and Fedora 20. You also need to install
  the Python 3 bindings and development files for GTK+.

  * **Ubuntu 16.04 / Debian 9** ``sudo apt-get install python3-dev python3-gi python3-gi-cairo libgirepository1.0-dev libcairo2-dev libpango1.0-dev libwebkitgtk-3.0-0 gir1.2-webkit2-3.0``

  * **Ubuntu 18.04, 20.04 / Debian 10, 11** ``sudo apt-get install python3-dev python3-gi python3-gi-cairo libgirepository1.0-dev libcairo2-dev libpango1.0-dev libwebkit2gtk-4.0-37 gir1.2-webkit2-4.0``

  * **Fedora** ``sudo dnf install pygobject3 python3-gobject python3-cairo-devel cairo-gobject-devel gobject-introspection-devel pywebkitgtk``

  * **Arch / Manjaro** ``sudo pacman -Syu git pkgconf cairo python-cairo pango gobject-introspection gobject-introspection-runtime python-gobject webkit2gtk``

* If you're on Windows, you'll need Windows 10 or newer. If you are using
  Windows 10 and want to use a WebView to display web content, you will also
  need to install the [Edge WebView2 Evergreen
  Runtime.](https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section)
  Windows 11 has this runtime installed by default.

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

* `@pybeeware on Twitter <https://twitter.com/pybeeware>`__

* `Discord <https://beeware.org/bee/chat/>`__

* The Toga `Github Discussions forum <https://github.com/beeware/toga/discussions>`__

Contributing
~~~~~~~~~~~~

If you'd like to contribute to Toga development, our `guide for first time
contributors`_ will help you get started.

If you experience problems with Toga, `log them on GitHub`_. If you want to
contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: https://beeware.org/
.. _Read The Docs: https://toga.readthedocs.io
.. _guide for first time contributors: https://toga.readthedocs.io/en/latest/how-to/contribute.html
.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls
.. _Virtual Environment: https://www.virtualenv.org
