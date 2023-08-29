Tree
====

A widget for displaying a hierarchical tree of tabular data. Scroll bars will be
provided if necessary.

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

The simplest way to create a Tree is to pass a dictionary and a list of column headings.
Each key in the dictionary can be either a tuple, whose contents will be mapped
sequentially to the columns of a node, or a single object, which will be mapped to the
first column. And each value in the dictionary can be either another dictionary
containing the children of that node, or ``None`` if there are no children.

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
providing data values. This allows you to store data in the data source that
won't be displayed in the tree. It also allows you to control the display order of
columns independent of the storage of that data.

.. code-block:: python

    import toga

    tree = toga.Tree(
        headings=["Name", "Age"],
        data=[
            (
                {"name": "Earth"},
                [({"name": "Arthur Dent", "age": 42, "status": "Anxious"}, None)]
            ),
            (
                {"name": "Betelgeuse Five"},
                [
                    ({"name": "Ford Prefect", "age": 37, "status": "Hoopy"}, None),
                    ({"name": "Zaphod Beeblebrox", "age": 47, "status": "Oblivious"}, None),
                ]
            ),
        ]
    )

    # Get the details of the first child of the second root node:
    node = tree.data[1][0]
    print(f"{node.name}, who is age {node.age}, is {node.status}")

.. include:: table-accessors.rst

If you want to use different attributes, you can override them by providing an
``accessors`` argument. In this example, the tree will use "Name" as the visible header,
but internally, the attribute "character" will be used:

.. code-block:: python

    import toga

    tree = toga.Tree(
        headings=["Name", "Age"],
        accessors={"Name", 'character'},
        data=[
            (
                {"character": "Earth"},
                [({"character": "Arthur Dent", "age": 42, "status": "Anxious"}, None)]
            ),
            (
                {"character": "Betelgeuse Five"},
                [
                    ({"character": "Ford Prefect", "age": 37, "status": "Hoopy"}, None),
                    ({"character": "Zaphod Beeblebrox", "age": 47, "status": "Oblivious"}, None),
                ]
            ),
        ]
    )

    # Get the details of the first child of the second root node:
    node = tree.data[1][0]
    print(f"{node.character}, who is age {node.age}, is {node.status}")

.. include:: table-values.rst

Notes
-----

* Widgets in cells is a beta API which may change in future, and is currently only
  supported on macOS.

* On macOS, you cannot change the font used in a Tree.


Reference
---------

.. autoclass:: toga.Tree
