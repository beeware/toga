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

The backend for macOS is named `toga-cocoa`_. It supports macOS 10.10 (Yosemite)
and later. It is installed automatically on macOS machines (machines that
report ``sys.platform == 'darwin'``), or can be manually installed by invoking:

.. code-block:: console

    $ pip install toga-cocoa

The macOS backend has seen the most development to date. It uses `Rubicon`_ to
provide a bridge to native macOS libraries.

.. _toga-cocoa: https://github.com/beeware/toga/tree/main/cocoa
.. _Rubicon: https://github.com/beeware/rubicon-objc

Linux
~~~~~

.. image:: /reference/screenshots/gtk.png

The backend for Linux platforms is named `toga-gtk`_. It supports GTK 3.4
and later. It is installed automatically on Linux machines (machines that
report ``sys.platform == 'linux'``), or can be manually installed by
invoking:

.. code-block:: console

    $ pip install toga-gtk

The GTK backend is reasonably well developed, but currently has some known issues
with widget layout. It uses the native GObject Python bindings.

.. _toga-gtk: https://github.com/beeware/toga/tree/main/gtk

Windows
~~~~~~~~

.. image:: /reference/screenshots/winforms.png

The backend for Windows is named `toga-winforms`_. It supports Windows 11 with
.NET 4 installed. It is installed automatically on Windows machines
(machines that report ``sys.platform == 'win32'``), or can be manually
installed by invoking:

.. code-block:: console

    $ pip install toga-winforms

It uses `Python.net`_.

.. _toga-winforms: https://github.com/beeware/toga/tree/main/winforms
.. _Python.net: https://pythonnet.github.io

Mobile platforms
----------------

iOS
~~~

The backend for iOS is named `toga-iOS`_. It supports iOS 6 or later. It
must be manually installed into an iOS Python project. It can be manually
installed by invoking:

.. code-block:: console

    $ pip install toga-iOS

The iOS backend is currently proof-of-concept only. Most widgets have not been
implemented. It uses `Rubicon`_ to provide a bridge to native macOS libraries.

.. _toga-iOS: https://github.com/beeware/toga/tree/main/iOS

Android
~~~~~~~

The backend for Android is named `toga-android`_. It can be manually installed
by invoking:

.. code-block:: console

    $ pip install toga-android

The android backend is currently proof-of-concept only. Most widgets have not
been implemented. It uses `Chaquopy`_ to provide a way to access the Android
Java libraries and implement Java interfaces in Python.

.. _toga-android: https://github.com/beeware/toga/tree/main/android
.. _Chaquopy: https://chaquo.com/chaquopy/

Web
---

The Web backend is named `toga-web`_. It can be manually installed
by invoking:

.. code-block:: console

    $ pip install toga-web

The Web backend is currently proof-of-concept only. Most widgets have not been
implemented. It uses `PyScript`_ to run Python code in the browser.

.. _toga-web: https://github.com/beeware/toga/tree/main/web
.. _PyScript: https://pyscript.net

The Dummy platform
------------------

Toga also provides a Dummy platform - this is a backend that implements the full
interface required by a platform backend, but does not display any widgets visually.
It is intended for use in tests, and provides an API that can be used to verify
widget operation.

Planned platform support
========================

Eventually, the Toga project would like to provide support for the following platforms:

 * UWP (Native Windows 8 and Windows mobile)
 * Qt (for KDE based desktops)
 * tvOS (for AppleTV devices)
 * watchOS (for AppleWatch devices)
 * Curses (for console)

If you are interested in these platforms and would like to contribute, please
get in touch on `Mastodon <https://fosstodon.org/@beeware>`__ or
`Discord <https://beeware.org/bee/chat/>`__.


Unofficial platform support
===========================

At present, there are no known unofficial platform backends.
