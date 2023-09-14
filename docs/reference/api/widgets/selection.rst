Selection
=========

A widget to select a single option from a list of alternatives.

.. figure:: /reference/images/Selection.png
    :align: center

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
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

    # Change the selection to "Charlie"
    selection.value = "Charlie"

    # Which item is currently selected? This will print "Charlie"
    print(f"Currently selected: {selection.value}")


A Selection can also be used to display a list of dictionaries, with the
``accessor`` detailing which attribute of the dictionary will be used for
display purposes. When the current value of the widget is retrieved, a Row
object will be returned; this Row object will have all the original data as
attributes on the Row. In the following example, the GUI will only display the
names in the list of items, but the age will be available as an attribute on the
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

    # Select Bob explicitly
    selection.value = selection.items[1]

    # What is the age of the currently selected person? This will print 42
    print(f"Age of currently selected person: {selection.value.age}")

    # Select Charlie by searching
    selection.value = selection.items.find(name="Charlie")

Notes
-----

* On macOS and Android, you cannot change the font of a Selection.

* On macOS, GTK and Android, you cannot change the text color, background color, or
  alignment of labels in a Selection.

* On GTK, a Selection widget with flexible sizing will expand its width (to the
  extent possible possible) to accommodate any changes in content (for example,
  to accommodate a long label). However, if the content subsequently *decreases*
  in width, the Selection widget *will not* shrink. It will retain the size
  necessary to accommodate the longest label it has historically contained.

* On iOS, the size of the Selection widget does not adapt to the size of the
  currently displayed content, or the potential list of options.

Reference
---------

.. autoclass:: toga.Selection
