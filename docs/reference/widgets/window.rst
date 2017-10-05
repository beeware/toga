:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Window
======

A window for displaying components to the user

Usage
-----

The window class is used for desktop applications, where components need to be shown within a window-manager. Windows can be configured on
instantiation and support displaying multiple widgets, toolbars and resizing.

.. code-block:: Python

    import toga

    window = toga.Window('my window', title='This is a window!')
    window.show()

Supported Platforms
-------------------

.. include:: ../supported_platforms/Window.rst

Reference
---------

.. autoclass:: toga.window.Window
   :members:
   :undoc-members:
   :inherited-members: