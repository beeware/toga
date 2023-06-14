ListSource
==========

A data source describing an ordered list of data.

Usage
-----

Data sources are abstractions that allow you to define the data being managed by
your application independent of the GUI representation of that data.

ListSource is an implementation of an ordered list of data. When a ListSource is
created, it is given a list of ``accessors`` - these are the attributes that
all items managed by the ListSource will have.

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

The ListSource manages a list of Rows. Each Row object in the ListSource is an
object that has all the attributes described by the ``accessors``. A Row object
will be constructed by the source for each item that is added or removed from
the ListSource.

Most importantly, other objects can subscribe to the ListSource and be notified
of any changes. This allows a GUI widget (or multiple GUI widgets) to listen to
the ListSource, and update their graphical representation in response to data
being added or removed from the source.

Although Toga provides ListSource, you are not required to use it. A ListSource
will be transparently constructed for you if you provide a Python ``list``
object to a GUI widget that displays list-like data (e.g., Table or Selection);
however, any object that adheres to the same interface can be used as an
alternative source of data for widgets that support using a ListSource.

Reference
---------

.. autoclass:: toga.sources.ListSource
   :members:
   :undoc-members:
