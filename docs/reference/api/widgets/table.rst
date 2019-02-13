Table
=====

======= ====== ========= ===== ========= ========
 macOS   GTK+   Windows   iOS   Android   Django
======= ====== ========= ===== ========= ========
 |y|     |y|    |y|
======= ====== ========= ===== ========= ========

.. |y| image:: /_static/yes.png
    :width: 16

The table widget is a widget for displaying tabular data. It can be instantiated with the list of headings and then data rows
can be added.

.. figure:: /reference/images/Table1.jpeg
    :align: center

Usage
-----

.. code-block:: Python

    import toga

    table = toga.Table(['Heading 1', 'Heading 2'])

    # Append to end of table
    table.data.append('Value 1', 'Value 2')

    # Insert to row 2
    table.data.insert(2, 'Value 1', 'Value 2')

Reference
---------

.. autoclass:: toga.widgets.table.Table
   :members:
   :undoc-members:
   :inherited-members:
