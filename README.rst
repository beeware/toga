Toga
====

A Python native, OS native GUI toolkit.

Prerequisites
~~~~~~~~~~~~~

Toga has some minimum requirements:

* Toga requires **Python 3**. Python 2 is not supported.

* If you're on macOS, you need to be on 10.7 (Lion) or newer.

* If you're on Linux, you need to have GTK+ 3.10 or later. This is the version
  that ships starting with Ubuntu 14.04 and Fedora 20. You also need to install
  the Python 3 bindings to GTK+. If you want to use the WebView widget, you'll
  also need to have WebKit, plus the GI bindings to WebKit installed. This means
  you'll need to install the following:

  * **Ubuntu 14.04** ``apt-get install python3-gi gir1.2-webkit-3.0``

  * **Ubuntu 16.04** ``apt-get install python3-gi gir1.2-webkit-4.0``
    or ``apt-get install python3-gi gir1.2-webkit-3.0``

  * **Debian** ??

  * **Fedora** ??

If these requirements aren't met, Toga either won't work at all, or won't have
full functionality.

Quickstart
----------

To get a demonstration of the capabilities of Toga, run the following::

    $ pip install toga-demo
    $ toga-demo

This will pop up a GUI window with some sample widgets.

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

* The `pybee/general`_ channel on Gitter.

Contributing
------------

If you experience problems with Toga, `log them on GitHub`_. If you
want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _BeeWare suite: http://pybee.org
.. _Read The Docs: https://toga.readthedocs.io
.. _toga-cocoa: http://github.com/pybee/toga-cocoa
.. _toga-gtk: http://github.com/pybee/toga-gtk
.. _toga-win32: http://github.com/pybee/toga-win32
.. _toga-iOS: http://github.com/pybee/toga-iOS
.. _toga-android: http://github.com/pybee/toga-android
.. _@pybeeware on Twitter: https://twitter.com/pybeeware
.. _pybee/general: https://gitter.im/pybee/general
.. _log them on Github: https://github.com/pybee/toga/issues
.. _fork the code: https://github.com/pybee/toga
.. _submit a pull request: https://github.com/pybee/toga/pulls
