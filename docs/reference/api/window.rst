Window
======

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|       |y|   |y|       |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 32

A window for displaying components to the user

Usage
-----

The window class is used for desktop applications, where components need to be shown within a window-manager. Windows can be configured on
instantiation and support displaying multiple widgets, toolbars and resizing.

.. code-block:: Python

    import toga

    window = toga.Window('my window', title='This is a window!')
    window.show()

Reference
---------

.. autoclass:: toga.window.Window
   :members:
   :undoc-members:
   :inherited-members:
