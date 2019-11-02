Table
=====

.. rst-class:: widget-support
.. csv-filter::
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Table|Component)$)'}

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
