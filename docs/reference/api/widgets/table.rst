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

A Table uses a :class:`~toga.sources.ListSource` to manage the data being displayed.
options. If ``data`` is not specified as a ListSource, it will be converted into a
ListSource at runtime.

The simplest instantiation of a Table is to use a list of lists (or list of tuples),
containing the items to display in the table. When creating the table, you must also
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

You can also specify data for a Table using a list of dictionaries. This allows to to
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
    print(f"{table.data[0].name}, who is age {table.data[0].age}, is from {table.data[0].planet}")

The attribute names used on each row of data (called "accessors") are created automatically from
the name of the headings that you provide. This is done by:

1. Converting the heading to lower case;
2. Removing any character that can't be used in a Python identifier;
3. Replacing all whitespace with "_";
4. Prepending ``_`` if the first character is a digit.

If you want to use different accessors to the ones that are automatically generated, you
can override them by providing an ``accessors`` argument. This can be either:

* A list of the same size as the list of headings, specifying the accessors for each
  heading. A value of :any:`None` will fall back to the default generated accessor; or
* A dictionary mapping heading names to accessor names.

In this example, the table will use "Name" as the visible header, but internally, the
attribute "character" will be used:

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
    print(f"{table.data[0].character}, who is age {table.data[0].age}, is from {table.data[0].planet}")

You can also create a table *without* a heading row. However, if you do this, you *must*
specify accessors.

If the value provided by an accessor is :any:`None`, or the accessor isn't defined for a
given row, the value of ``missing_value`` provided when constructing the Table will
be used to populate the cell in the Table.

If the value provided by an accessor is any type other than a tuple :any:`tuple` or
:any:`toga.Widget`, the value will be converted into a string. If the value has an
``icon`` attribute, the cell will use that icon in the Table cell, displayed to the left
of the text label. If the value of the ``icon`` attribute is :any:`None`, no icon will
be displayed.

If the value provided by an accessor is a :any:`tuple`, the first element in the tuple
must be an :class:`toga.Icon`, and the second value in the tuple will be used to provide
the text label (again, by converting the value to a string, or using ``missing_value``
if the value is :any:`None`, as appropriate).

If the value provided by an accessor is a :class:`toga.Widget`, that widget will be displayed
in the table. Note that this is currently a beta API, and may change in future.

Notes
-----

* The use of Widgets as table values is currently a beta API. It is currently only
  supported on macOS; the API is subject to change.

Reference
---------

.. autoclass:: toga.Table
   :members:
   :undoc-members:
