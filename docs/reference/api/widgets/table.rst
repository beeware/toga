Table
=====

A widget for displaying columns of tabular data. Scroll bars will be provided if
necessary.

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

The simplest way to create a Table is to pass a list of tuples containing the items to
display, and a list of column headings. The values in the tuples will then be mapped
sequentially to the columns.

In this example, we will display a table of 2 columns, with 3 initial rows of data:

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
            {"name": "Tricia McMillan", "age": 38, "planet": "Earth"},
        ]
    )

    # Get the details of the first item in the data:
    row = table.data[0]
    print(f"{row.name}, who is age {row.age}, is from {row.planet}")

.. include:: table-accessors.rst

If you want to use different attributes, you can override them by providing an
``accessors`` argument. In this example, the table will use "Name" as the visible
header, but internally, the attribute "character" will be used:

.. code-block:: python

    import toga

    table = toga.Table(
        headings=["Name", "Age"],
        accessors={"Name", 'character'},
        data=[
            {"character": "Arthur Dent", "age": 42, "planet": "Earth"},
            {"character", "Ford Prefect", "age": 37, "planet": "Betelgeuse Five"},
            {"name": "Tricia McMillan", "age": 38, "planet": "Earth"},
        ]
    )

    # Get the details of the first item in the data:
    row = table.data[0]
    print(f"{row.character}, who is age {row.age}, is from {row.planet}")

.. include:: table-values.rst

Notes
-----

* Widgets in cells is a beta API which may change in future, and is currently only
  supported on macOS.

* macOS does not support changing the font used to render table content.

* On Winforms, icons are only supported in the first column. On Android, icons are not
  supported at all.

* The Android implementation is `not scalable
  <https://github.com/beeware/toga/issues/1392>`_ beyond about 1,000 cells.

Reference
---------

.. autoclass:: toga.Table
