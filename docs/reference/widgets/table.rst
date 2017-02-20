Table
=====

The table widget is a widget for displaying tabular data. It can be instantiated with the list of headings and then data rows
can be added.

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

.. autoclass:: toga.interface.widgets.table.Table
   :members:
   :undoc-members:
   :inherited-members: