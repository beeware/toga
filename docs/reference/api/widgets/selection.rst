Selection
=========

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|     |y|      |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The Selection widget is a simple control for allowing the user to choose between a list of string options.

.. figure:: /reference/images/Selection.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    container = toga.Selection(items=['bob', 'jim', 'lilly'])

Reference
---------

.. autoclass:: toga.widgets.selection.Selection
   :members:
   :undoc-members:
   :inherited-members:
