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

``toga-winforms`` requires Windows 10 or newer.

If you are using Windows 10 and want to use a WebView to display web content, you will
also need to install the `Edge WebView2 Evergreen Runtime.
<https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section>`__
Windows 11 has this runtime installed by default.

Installation
------------

``toga-winforms`` is installed automatically on Windows machines (machines that report ``sys.platform
== 'win32'``), or can be manually installed by running:

.. code-block:: console

    $ python -m pip install toga-winforms

Implementation details
----------------------

``toga-winforms`` uses `Python.net <https://pythonnet.github.io>`__.
