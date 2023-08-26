Tree
====

A widget for displaying a hierarchical tree of tabular data.

.. figure:: /reference/images/Tree.png
   :width: 300px
   :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!^(Tree|Component)$)'}

Usage
-----

A Tree uses a :class:`~toga.sources.TreeSource` to manage the data being displayed.
options. If ``data`` is not specified as a TreeSource, it will be converted into a
TreeSource at runtime.

The simplest instantiation of a Tree is to use a dictionary, where the keys are the data
for each node, and the values describe the children for that node. When creating the
Tree, you must also specify the headings to use on the tree; those headings will be
converted into accessors on the Node data objects created for the tree data. The values
in the tuples provided as keys in the data will then be mapped sequentially to the
accessors; or, if an atomic value has been provided as a key, only the first accessor
will be populated.

In this example, we will display a tree with 2 columns. The tree will have 2 root
nodes; the first root node will have 1 child node; the second root node will have 2
children. The root nodes will only populate the "name" column; the other column will be
blank:

.. code-block:: python

    import toga

    tree = toga.Tree(
        headings=["Name", "Age"],
        data={
            "Earth": {
               ("Arthur Dent", 42): None,
            },
            "Betelgeuse Five": {
               ("Ford Prefect", 37): None,
               ("Zaphod Beeblebrox", 47): None,
            },
        }
    )

    # Get the details of the first child of the second root node:
    print(f"{tree.data[1][0].name} is age {tree.data[1][0].age}")

    # Append new data to the first root node in the tree
    tree.data[0].append(("Tricia McMillan", 38))

You can also specify data for a Tree using a list of 2-tuples, with dictionaries
providing serving as data values. This allows to to store data in the data source that
won't be displayed in the tree. It also allows you to control the display order of
columns independent of the storage of that data.

.. code-block:: python

    import toga

    tree = toga.Tree(
        headings=["Name", "Age"],
        data=[
            ({"name": "Earth"}), [
               ({"name": "Arthur Dent", "age": 42, "status": "Anxious"}, None)
            ],
            ({"name": "Betelgeuse Five"}), [
               ({"name": "Ford Prefect", "age": 37, "status": "Hoopy"}, None)
               ({"name": "Zaphod Beeblebrox", "age": 47, "status": "Oblivious"}, None)
            ],
        ]
    )

    # Get the details of the first child of the second root node:
    print(f"{tree.data[1][0].name} is age {tree.data[1][0].age}")

    # Append new data to the first root node in the tree
    tree.data[0].append({"name": "Tricia McMillan", "age": 38, "status": "Overqualified"})

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

In this example, the tree will use "Name" as the visible header, but internally, the
attribute "character" will be used:

.. code-block:: python

    import toga

    tree = toga.Tree(
        headings=["Name", "Age"],
        accessors={"Name", 'character'},
        data=[
            ({"character": "Earth"}), [
               ({"character": "Arthur Dent", "age": 42, "status": "Anxious"}, None)
            ],
            ({"character": "Betelgeuse Five"}), [
               ({"character": "Ford Prefect", "age": 37, "status": "Hoopy"}, None)
               ({"character": "Zaphod Beeblebrox", "age": 47, "status": "Oblivious"}, None)
            ],
        ]
    )

    # Get the details of the first child of the second root node:
    print(f"{tree.data[1][0].character} is age {tree.data[1][0].age}")

    # Get the details of the first item in the data:
    print(f"{tree.data[0].character}, who is age {tree.data[0].age}, is from {tree.data[0].planet}")

You can also create a tree *without* a heading row. However, if you do this, you *must*
specify accessors.

If the value provided by an accessor is :any:`None`, or the accessor isn't defined for a
given row, the value of ``missing_value`` provided when constructing the Tree will
be used to populate the cell in the Tree.

If the value provided by an accessor is any type other than a tuple :any:`tuple` or
:any:`toga.Widget`, the value will be converted into a string. If the value has an
``icon`` attribute, the cell will use that icon in the Tree cell, displayed to the left
of the text label. If the value of the ``icon`` attribute is :any:`None`, no icon will
be displayed.

If the value provided by an accessor is a :any:`tuple`, the first element in the tuple
must be an :class:`toga.Icon`, and the second value in the tuple will be used to provide
the text label (again, by converting the value to a string, or using ``missing_value``
if the value is :any:`None`, as appropriate).

If the value provided by an accessor is a :class:`toga.Widget`, that widget will be displayed
in the tree. Note that this is currently a beta API, and may change in future.


Notes
-----

* The use of Widgets as tree values is currently a beta API. It is currently only
  supported on macOS; the API is subject to change.

* On macOS, you cannot change the font used in a Tree.


Reference
---------

.. autoclass:: toga.Tree
   :members:
   :undoc-members:
