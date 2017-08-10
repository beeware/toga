:orphan:

.. warnings about this file not being included in any toctree will be suppressed by :orphan:

Table
=====

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
    table.insert(None, 'Value 1', 'Value 2')
    
    # Insert to row 2
    table.insert(2, 'Value 1', 'Value 2')

Supported Platforms
-------------------

.. include:: ../supported_platforms/Table.rst

Reference
---------

.. autoclass:: toga.widgets.table.Table
   :members:
   :undoc-members:
   :inherited-members: