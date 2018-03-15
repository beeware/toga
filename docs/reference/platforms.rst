========================
Toga supported platforms
========================

Official platform support
=========================

Desktop platforms
-----------------

OS X
~~~~

.. image:: /reference/screenshots/cocoa.png

The backend for OS X is named `toga_cocoa`_. It supports OS X 10.7 (Lion)
and later. It is installed automatically on OS X machines (machines that
report ``sys.platform == 'darwin'``), or can be manually installed by invoking::

    $ pip install toga[cocoa]

The OS X backend has seen the most development to date.

.. _toga_cocoa: https://github.com/pybee/toga/tree/master/src/cocoa

Linux
~~~~~

.. image:: /reference/screenshots/gtk.png

The backend for Linux platforms is named `toga_gtk`_. It supports GTK+ 3.4
and later. It is installed automatically on Linux machines (machines that
report ``sys.platform == 'linux'``), or can be manually installed by
invoking::

    $ pip install toga[gtk]

The GTK+ backend is reasonably well developed, but currently has some known issues
with widget layout.

.. _toga_gtk: https://github.com/pybee/toga/tree/master/src/gtk

Winforms
~~~~~~~~

The backend for Windows is named `toga_winforms`_. It supports Windows XP or
later with .NET installed. It is installed automatically on Windows machines
(machines that report ``sys.platform == 'win32'``), or can be manually
installed by invoking::

    $ pip install toga[winforms]

The Windows backend is currently proof-of-concept only. Most widgets have not been
implemented.

.. _toga_winforms: https://github.com/pybee/toga/tree/master/src/winforms

Mobile platforms
----------------

iOS
~~~

The backend for iOS is named `toga_iOS`_. It supports iOS 6 or later. It
must be manually installed into an iOS Python project (such as one that has
been developed using the `Python-iOS-template cookiecutter`_). It can be
manually installed by invoking::

    $ pip install toga[iOS]

The iOS backend is currently proof-of-concept only. Most widgets have not been
implemented.

.. _Python-iOS-template cookiecutter: http://github.com/pybee/Python-iOS-template
.. _toga_iOS: http://github.com/pybee/toga/tree/master/src/iOS

Android
~~~~~~~

The backend for Android is named `toga_android`_. It can be manually installed
by invoking::

    $ pip install toga[android]

The android backend is currently proof-of-concept only. Most widgets have not been
implemented.

.. _toga_android: http://github.com/pybee/toga/tree/master/src/android

Planned platform support
========================

There are plans to provide support for the following platforms:

 * Web (using Batavia_ to run Python on the browser)
 * Android
 * WinRT (Native Windows 8 and Windows mobile)
 * Qt (for KDE based desktops)

If you are interested in these platforms and would like to contribute, please
get in touch on Twitter_ or Gitter_.

.. _Batavia: https://github.com/pybee/batavia
.. _Twitter: https://twitter.com/pybeeware
.. _Gitter: https://gitter.im/pybee/general

Unofficial platform support
===========================

At present, there are no known unofficial platform backends.

