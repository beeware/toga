=====
macOS
=====

.. image:: /reference/screenshots/cocoa.png
   :align: center
   :width: 300

The Toga backend for macOS is `toga-cocoa
<https://github.com/beeware/toga/tree/main/cocoa>`__.

.. _macos-prerequisites:

Prerequisites
-------------

``toga-cocoa`` requires Python 3.9+, and macOS 11 (Big Sur) or newer.

Installation
------------

``toga-cocoa`` is installed automatically on macOS machines (machines that report
``sys.platform == 'darwin'``), or can be manually installed by running invoking:

.. code-block:: console

    $ python -m pip install toga-cocoa

Implementation details
----------------------

The ``toga-cocoa`` backend uses the `AppKit Objective-C API
<https://developer.apple.com/documentation/appkit/>`__, also known as Cocoa.

The native APIs are accessed using `Rubicon Objective C
<https://rubicon-objc.readthedocs.io/>`__.
