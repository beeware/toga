=======================
Toga supported plaforms
=======================

Official platform support
=========================

Desktop platforms
-----------------

OS X
~~~~

.. image:: screenshots/cocoa.png

The backend for OS X is named `toga-cocoa`_. It supports OS X 10.7 (Lion)
and later. It is installed automatically on OS X machines (machines that
report ``sys.platform == 'darwin'``), or can be manually installed by invoking::

    $ pip install toga[cocoa]

The OS X backend has seen the most development to date.

.. _toga-cocoa: http://github.com/pybee/toga-cocoa

Linux
~~~~~

.. image:: screenshots/gtk.png

The backend for Linux platforms is named `toga-gtk`_. It supports GTK+ 3.4
and later. It is installed automatically on Linux machines (machines that
report ``sys.platform in ('linux', 'linux2')``), or can be manually installed by
invoking::

    $ pip install toga[gtk]

The GTK+ backend is reasonably well developed, but currently has some known issues
with widget layout.

.. _toga-gtk: http://github.com/pybee/toga-gtk

Win32
~~~~~

The backend for Windows is named `toga-win32`_. It supports Windows XP or
later. It is installed automatically on Windows machines (machines that report
``sys.platform == 'win32'``), or can be manually installed by invoking::

    $ pip install toga[win32]

The Windows backend is currently proof-of-concept only. Most widgets have not been
implemented.

.. _toga-win32: http://github.com/pybee/toga-win32

Mobile platforms
----------------

iOS
~~~

The backend for iOS is named `toga-iOS`_. It supports iOS 6 or later. It
must be manually installed into an iOS Python project (such as one that has
been developed using the `Python-iOS-template cookiecutter`_). It can be
manually installed by invoking::

    $ pip install toga[iOS]

The iOS backend is currently proof-of-concept only. Most widgets have not been
implemented.

.. _Python-iOS-template cookiecutter: http://github.com/pybee/Python-iOS-template
.. _toga-iOS: http://github.com/pybee/toga-iOS


Planned platform support
========================

There are plans to provide support for the following platforms:

 * Android
 * WinRT (Native Windows 8 and Windows mobile)
 * Qt (for KDE based desktops)

If you are interested in these platforms and would like to contribute, please
`get in touch using the beeware-developers mailing list`_.

.. _get in touch using the beeware-developers mailing list: https://groups.google.com/forum/#!forum/beeware-developers

Unofficial platform support
===========================

At present, there are no known unofficial platform backends.

