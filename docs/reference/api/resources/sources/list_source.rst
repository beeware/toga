ListSource
==========

A data source describing an ordered list of data.

Usage
-----

Data sources are abstractions that allow you to define the data being managed by your
application independent of the GUI representation of that data. For details on the use
of data sources, see the :doc:`background guide </background/topics/data-sources>`.

ListSource is an implementation of an ordered list of data. When a ListSource is
created, it is given a list of ``accessors`` - these are the attributes that all items
managed by the ListSource will have. The API provided by ListSource is :any:`list`-like;
the operations you'd expect on a normal Python list, such as ``insert``, ``remove``,
``index``, and indexing with ``[]``, are also possible on a ListSource:

.. code-block:: python

    from toga.sources import ListSource

    source = ListSource(
        accessors=["name", "weight"],
        data=[
            {"name": "Platypus", "weight": 2.4},
            {"name": "Numbat", "weight": 0.597},
            {"name": "Thylacine", "weight": 30.0},
        ]
    )

    # Get the first item in the source
    item = source[0]
    print(f"Animal's name is {item.name}")

    # Find an item with a name of "Thylacine"
    item = source.find({"name": "Thylacine"})

    # Remove that item from the data
    source.remove(item)

    # Insert a new item at the start of the data
    source.insert(0, {"name": "Bettong", "weight": 1.2})

.. _listsource-item:

When initially constructing the ListSource, or when assigning a specific item in
the ListSource, each item can be:

* A dictionary, with the accessors mapping to the keys in the dictionary

* Any iterable object (except for a string), with the accessors being mapped
  onto the items in the iterable in order of definition

* Any other object, which will be mapped onto the *first* accessor.

The ListSource manages a list of :class:`~toga.sources.Row` objects. Each Row object in
the ListSource is an object that has all the attributes described by the ``accessors``.
A Row object will be constructed by the source for each item that is added or removed
from the ListSource.

When creating a single Row for a ListSource (e.g., when inserting a new
item), the data for the Row can be specified as:

* A dictionary, with the accessors mapping to the keys in the dictionary

* Any iterable object (except for a string), with the accessors being mapped
  onto the items in the iterable in order of definition. This requires that the
  iterable object have *at least* as many values as the number of accessors
  defined on the TreeSource.

* Any other object, which will be mapped onto the *first* accessor.

When initially constructing the ListSource, the data must be an iterable of values, each
of which can be converted into a Row.

Although Toga provides ListSource, you are not required to use it directly. A ListSource
will be transparently constructed for you if you provide a Python ``list`` object to a
GUI widget that displays list-like data (i.e., :class:`toga.Table`,
:class:`toga.Selection`, or :class:`toga.DetailedList`).

Custom List Sources
-------------------

For more complex applications, you can replace ListSource with a :ref:`custom data
source <custom-data-sources>` class. Such a class must:

* Inherit from :any:`Source`

* Provide the same methods as :any:`ListSource`

* Return items whose attributes match the accessors for any widget using the source

* Generate a ``change`` notification when any of those attributes change

* Generate ``insert``, ``remove`` and ``clear`` notifications when items are added or
  removed

Reference
---------

.. autoclass:: toga.sources.Row
   :special-members: __setattr__

.. autoclass:: toga.sources.ListSource
   :special-members: __len__, __getitem__, __setitem__, __delitem__
