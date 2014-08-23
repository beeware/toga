Toga
====

A Python native, OS native GUI toolkit.

Quickstart
----------

To get a demonstration of the capabilities of Toga, run the following::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window with some sample widgets.

Prerequisites
~~~~~~~~~~~~~

Toga has some minimum requirements:

* If you're on OS X, you need to be on 10.7 (Lion) or newer.

* If you're on Linux, you need to have GTK+ 3.4 or later. This is the
  version that ships with Ubuntu 12.04. If you want to use the WebView
  widget, you'll also need to have WebKit, plus the GI bindings to WebKit
  (``gir1.2-webkit-3.0``) installed.

If these requirements aren't met, Toga either won't work at all, or won't
have full functionality.

Problems with source installs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Internally, Toga is comprised of a number of subpackages - one for each
platform it supports. If you install using wheels, the install process will
correctly identify the required packages and install them. However, if you
install from source using pip, there is a `known bug in pip`_ that causes
dependencies to not be installed. It may be necessary to manually install
the following pre-requisites:

* OS X: ``pip install toga-cocoa``
* Linux: ``pip install toga-gtk toga-cassowary cassowary``
* Win32: ``pip install toga-win32 toga-cassowary cassowary``

.. _known bug in pip: https://github.com/pypa/pip/issues/1951

Problems using virtualenv under Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running under Linux, Toga uses the system native python GTK+3 bindings
for display purposes. However, if you're using a ``--no-site-packages``
virtualenv, the Python bindings for GTK won't be in your ``PYTHONPATH``.

Unfortunately, you can't ``pip install`` GTK+ bindings, so you have to use a
workaround. To make the system GTK+ bindings available to your virtualenv,
symlinking the ``gi`` module from the system dist-packages directory into your
virtualenv's site-packages::

    $ cd $VIRTUAL_ENV/lib/python2.7/site-packages
    $ ln -si /usr/lib/python2.7/dist-packages/gi


Documentation
-------------

Documentation for Toga can be found on `Read The Docs`_.

Related projects
----------------

This package is a top level package. It depends on the use of platform-specific
backends to provide real functionality:

* `toga-cocoa`_: for OS/X
* `toga-gtk`_: GTK+ backend for Linux desktops
* `toga-win32`_: for Windows desktops (limited support)
* `toga-iOS`_: for iOS devices (iPhone, iPad, iPod)
* `toga-android`_: for Android devices (limited support)

Community
---------

Toga is part of the `BeeWare suite`_. You can talk to the community through:

* `@pybeeware on Twitter`_

* The `BeeWare Users Mailing list`_, for questions about how to use the BeeWare suite.

* The `BeeWare Developers Mailing list`_, for discussing the development of new features in the BeeWare suite, and ideas for new tools for the suite.

Contributing
------------

If you experience problems with Toga, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: http://toga.readthedocs.org
.. _toga-cocoa: http://github.com/pybee/toga-cocoa
.. _toga-gtk: http://github.com/pybee/toga-gtk
.. _toga-win32: http://github.com/pybee/toga-win32
.. _toga-iOS: http://github.com/pybee/toga-iOS
.. _toga-android: http://github.com/pybee/toga-android
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _BeeWare Users Mailing list: https://groups.google.com/forum/#!forum/beeware-users
.. _BeeWare Developers Mailing list: https://groups.google.com/forum/#!forum/beeware-developers
.. _log them on Github: https://github.com/pybee/toga/issues
.. _fork the code: https://github.com/pybee/toga
.. _submit a pull request: https://github.com/pybee/toga/pulls
