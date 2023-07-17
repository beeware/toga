=====
macOS
=====

.. image:: /reference/screenshots/cocoa.png
   :align: center
   :width: 300

The Toga backend for macOS is `toga-cocoa
<https://github.com/beeware/toga/tree/main/cocoa>`__.

Prerequisites
-------------

``toga-cocoa`` requires macOS 10.10 (Yosemite) or newer.

Installation
------------

``toga-cocoa`` is installed automatically on macOS machines (machines that report
``sys.platform == 'darwin'``), or can be manually installed by running invoking:

.. code-block:: console

    $ python -m pip install toga-cocoa

Implementation details
----------------------

``toga-cocoa`` uses the macOS AppKit Objective-C APIs to build apps. It uses `Rubicon
Objective-C <https://rubicon-objc.readthedocs.org>`__ to provide a bridge to the native
AppKit libraries from Python.
