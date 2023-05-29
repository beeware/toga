Selection
=========

A widget to select an single option from a list of alternatives.

.. figure:: /reference/images/Selection.jpeg
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!^(Selection|Component)$)'}


Usage
-----

The Selection uses a :class:`~toga.sources.ListSource` to manage the list of
options. If ``items`` is not specified as a ListSource, it will be converted
into a ListSource at runtime.

The simplest instantiation of a Selection is to use a list of strings. If a list
of non-string objects are provided, they will be converted into a string for
display purposes, but the original data type will be retained when returning the
current value.

.. code-block:: python

    import toga

    selection = toga.Selection(items=["Alice", "Bob", "Charlie"])

    # Which item is currently selected?
    print(f"Currently selected: {selection.value}")

A Selection can also be used to display a list of dictionaries, with the
``accessor`` detailing which attribute of the dictionary will be used for
display purposes. When the current value of the widget is retrieved, a Row
object will be returned; this Row object will have all the original data as
attributes on the Row. In the following example, the GUI will only display the
names in the list of items, but the age will be availalbe as an attribute on the
selected item.

.. code-block:: python

    import toga

    selection = toga.Selection(
        items=[
            {"name": "Alice", "age": 37},
            {"name": "Bob", "age": 42},
            {"name": "Charlie", "age": 24},
        ],
        accessor="name",
    )

    # What is the age of the currently selected person?
    print(f"Age of currently selected person: {selection.value.age}")


Reference
---------

.. autoclass:: toga.widgets.selection.Selection
   :members:
   :undoc-members:
