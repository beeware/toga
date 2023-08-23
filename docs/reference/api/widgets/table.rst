Table
=====

A widget for displaying columns of tabular data.

.. figure:: /reference/images/Table.png
   :width: 300px
   :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(Table|Component)$)'}

Usage
-----

A Table will automatically provide scroll bars when necessary.

The simplest instantiation of a Table is to use a list of lists (or list of tuples),
containing the items to display in the table. When creating the table, you can also
specify the headings to use on the table; those headings will be converted into
accessors on the Row data objects created for the table data. In this example,
we will display a table of 2 columns, with 3 initial rows of data:

.. code-block:: python

    import toga

    table = toga.Table(
        headings=["Name", "Age"],
        data=[
            ("Arthur Dent", 42),
            ("Ford Prefect", 37),
            ("Tricia McMillan", 38),
        ]
    )

    # Get the details of the first item in the data:
    print(f"{table.data[0].name} is age {table.data[0].age}")

    # Append new data to the table
    table.data.append(("Zaphod Beeblebrox", 47))

You can also specify data for a Table using a list of dictionaries. This allows you to
store data in the data source that won't be displayed in the table. It also allows you
to control the display order of columns independent of the storage of that data.

.. code-block:: python

    import toga

    table = toga.Table(
        headings=["Name", "Age"],
        data=[
            {"name": "Arthur Dent", "age": 42, "planet": "Earth"},
            {"name", "Ford Prefect", "age": 37, "planet": "Betelgeuse Five"},
            {"name": "Tricia McMillan", "age": 38, "plaent": "Earth"},
        ]
    )

    # Get the details of the first item in the data:
    row = table.data[0]
    print(f"{row.name}, who is age {row.age}, is from {row.planet}")

The attribute names used on each row of data (called "accessors") are created
automatically from the headings that you provide. If you want to use different
attributes, you can override them by providing an ``accessors`` argument. In this
example, the table will use "Name" as the visible header, but internally, the attribute
"character" will be used:

.. code-block:: python

    import toga

    table = toga.Table(
        headings=["Name", "Age"],
        accessors={"Name", 'character'},
        data=[
            {"character": "Arthur Dent", "age": 42, "planet": "Earth"},
            {"character", "Ford Prefect", "age": 37, "planet": "Betelgeuse Five"},
            {"name": "Tricia McMillan", "age": 38, "plaent": "Earth"},
        ]
    )

    # Get the details of the first item in the data:
    row = table.data[0]
    print(f"{row.character}, who is age {row.age}, is from {row.planet}")

The value provided by an accessor is interpreted as follows:

* If the value is a :any:`Widget`, that widget will be displayed in the cell. Note that
  this is currently a beta API, is currently only supported on macOS, and may change in
  future.

* If the value is a :any:`tuple`, it must have two elements: an icon, and a second
  element which will be interpreted as one of the options below.

* If the value is ``None``, then ``missing_value`` will be displayed.

* Any other value will be converted into a string. If an icon has not already been
  provided in a tuple, it can also be provided using the value's ``icon`` attribute.

Icon values must either be an :any:`Icon`, which will be displayed on the left of the
cell, or ``None`` to display no icon.

Reference
---------

.. autoclass:: toga.Table
   :members:
   :undoc-members:
