Table
=====

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Table|Component)$)'}

The table widget is a widget for displaying tabular data. It can be instantiated with the list of headings and then data rows
can be added.

.. figure:: /reference/images/Table1.jpeg
    :align: center

Usage
-----

.. code-block:: python

    import toga

    table = toga.Table(['Heading 1', 'Heading 2'])

    # Append to end of table
    table.data.append('Value 1', 'Value 2')

    # Insert to row 2
    table.data.insert(2, 'Value 1', 'Value 2')

        Examples:
            >>> headings = ['Head 1', 'Head 2', 'Head 3']
            >>> data = []
            >>> table = Table(headings, data=data)

            Data can be in several forms. A list of dictionaries, where the keys match
            the heading names:

            >>> data = [{'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}),
            >>>         {'head_1': 'value 1', 'head_2': 'value 2', 'head_3': 'value3'}]

            A list of lists. These will be mapped to the headings in order:

            >>> data = [('value 1', 'value 2', 'value3'),
            >>>         ('value 1', 'value 2', 'value3')]

            A list of values. This is only accepted if there is a single heading.

            >>> data = ['item 1', 'item 2', 'item 3']
        """


Reference
---------

.. autoclass:: toga.Table
   :members:
   :undoc-members:
