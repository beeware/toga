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

    # Find a row with a name of "Thylacine"
    row = source.find(name="Thylacine")

    # Remove that row from the data
    source.remove(row)

    # Insert a new row at the start of the data
    source.insert(0, name="Bettong", weight=1.2)

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

Although Toga provides ListSource, you are not required to use it directly. A ListSource
will be transparently constructed for you if you provide a Python ``list`` object to a
GUI widget that displays list-like data (e.g., Table or Selection). Any object that
adheres to the same interface can be used as an alternative source of data for widgets
that support using a ListSource. See the background guide on :ref:`custom data sources
<custom-data-sources>` for more details.

Custom List Sources
-------------------

Any object that adheres to the :any:`collections.abc.MutableSequence` protocol can be
used as a data source. This means they must provide:

* ``__len__(self)`` returning the number of items in the list

* ``__getitem__(self, index)`` returning the item at position ``index`` of the list.

A custom ListSource must also generate ``insert``, ``remove`` and ``clear``
notifications when items are added or removed from the source.

Each item returned by the custom ListSource is required to expose attributes matching
the accessors for any widget using the source. Any change to the values of these attributes
must generate a ``change`` notification on any listener to the custom ListSource.

Reference
---------

.. autoclass:: toga.sources.Row
   :members:
   :undoc-members:

.. autoclass:: toga.sources.ListSource
   :members:
   :undoc-members:
