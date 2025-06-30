=======
Windows
=======

.. image:: /reference/screenshots/winforms.png
   :align: center
   :width: 300

The Toga backend for Windows is `toga-winforms
<https://github.com/beeware/toga/tree/main/winforms>`__.

.. _windows-prerequisites:

Prerequisites
-------------

``toga-winforms`` requires Python 3.9+, and Windows 10 or newer.

If you are using Windows 10 and want to use a WebView to display web content, you will
also need to install the `Edge WebView2 Evergreen Runtime.
<https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download>`__
Windows 11 has this runtime installed by default.

Installation
------------

``toga-winforms`` is installed automatically on Windows machines (machines that report ``sys.platform
== 'win32'``), or can be manually installed by running:

.. code-block:: console

    $ python -m pip install toga-winforms

Implementation details
----------------------

The ``toga-winforms`` backend uses the `Windows Forms API
<https://learn.microsoft.com/en-us/dotnet/desktop/winforms/?view=netdesktop-8.0>`__.

The native .NET APIs are accessed using `Python.NET <http://pythonnet.github.io>`__.
