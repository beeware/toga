========================
Toga supported platforms
========================

Official platform support
=========================

Desktop platforms
-----------------

macOS
~~~~~

.. image:: /reference/screenshots/cocoa.png

The backend for macOS is named `toga-cocoa`_. It supports macOS 10.7 (Lion)
and later. It is installed automatically on macOS machines (machines that
report ``sys.platform == 'darwin'``), or can be manually installed by invoking::

    $ pip install toga-cocoa

The macOS backend has seen the most development to date. It uses `Rubicon`_ to
provide a bridge to native macOS libraries.

.. _toga-cocoa: https://github.com/beeware/toga/tree/master/src/cocoa
.. _Rubicon: https://github.com/beeware/rubicon-objc

Linux
~~~~~

.. image:: /reference/screenshots/gtk.png

The backend for Linux platforms is named `toga-gtk`_. It supports GTK+ 3.4
and later. It is installed automatically on Linux machines (machines that
report ``sys.platform == 'linux'``), or can be manually installed by
invoking::

    $ pip install toga-gtk

The GTK+ backend is reasonably well developed, but currently has some known issues
with widget layout. It uses the native GObject Python bindings.

.. _toga-gtk: https://github.com/beeware/toga/tree/master/src/gtk

Winforms
~~~~~~~~

The backend for Windows is named `toga-winforms`_. It supports Windows XP or
later with .NET installed. It is installed automatically on Windows machines
(machines that report ``sys.platform == 'win32'``), or can be manually
installed by invoking::

    $ pip install toga-winforms

The Windows backend is currently proof-of-concept only. Most widgets have not been
implemented. It uses `Python.net`_

.. _toga-winforms: https://github.com/beeware/toga/tree/master/src/winforms
.. _Python.net: https://pythonnet.github.io

Mobile platforms
----------------

iOS
~~~

The backend for iOS is named `toga-iOS`_. It supports iOS 6 or later. It
must be manually installed into an iOS Python project (such as one that has
been developed using the `Python-iOS-template cookiecutter`_). It can be
manually installed by invoking::

    $ pip install toga-iOS

The iOS backend is currently proof-of-concept only. Most widgets have not been
implemented. It uses `Rubicon`_ to provide a bridge to native macOS libraries.

.. _Python-iOS-template cookiecutter: http://github.com/beeware/Python-iOS-template
.. _toga-iOS: http://github.com/beeware/toga/tree/master/src/iOS

Android
~~~~~~~

The backend for Android is named `toga-android`_. It can be manually installed
by invoking::

    $ pip install toga-android

The android backend is currently proof-of-concept only. Most widgets have not
been implemented. It uses `VOC`_ to compile Python code to Java class files
for execution on Android devices.

.. _toga-android: http://github.com/beeware/toga/tree/master/src/android
.. _VOC: http://github.com/beeware/voc

Web platforms
-------------

Django
~~~~~~

The backend for Django is named `toga-django`_. It can be manually installed
by invoking::

    $ pip install toga-django

The Django backend is currently proof-of-concept only. Most widgets have not been
implemented. It uses `Batavia`_ to run Python code in the browser.

.. _toga-django: http://github.com/beeware/toga/tree/master/src/django
.. _Batavia: https://github.com/beeware/batavia

The Dummy platform
------------------

Toga also provides a Dummy platform - this is a backend that implements the full
interface required by a platform backend, but does not display any widgets visually.
It is intended for use in tests, and provides an API that can be used to verify
widget operation.

Planned platform support
========================

Eventually, the Toga project would like to provide support for the following platforms:

 * Other Python web frameworks (e.g., Flask, Pyramid)
 * UWP (Native Windows 8 and Windows mobile)
 * Qt (for KDE based desktops)
 * tvOS (for AppleTV devices)
 * watchOS (for AppleWatch devices)
 * Curses (for console)

If you are interested in these platforms and would like to contribute, please
get in touch on Twitter_ or Gitter_.

.. _Twitter: https://twitter.com/pybeeware
.. _Gitter: https://gitter.im/beeware/general

Unofficial platform support
===========================

At present, there are no known unofficial platform backends.

