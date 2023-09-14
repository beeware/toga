ValueSource
===========

A data source describing a single value.

Usage
-----

Data sources are abstractions that allow you to define the data being managed by your
application independent of the GUI representation of that data. For details on the use
of data sources, see the :doc:`background guide </background/topics/data-sources>`.

ValueSource is an wrapper around a single atomic value.

.. code-block:: python

    from toga.sources import ValueSource

    source = ValueSource(42)

    # Get the value managed by the source
    print(f"Meaning of life, the universe, and everything is {source.value}")


Custom ValueSources
-------------------

A custom ValueSource has 3 requirements:

* It must have an ``accessor`` attribute that describes the name of the attribute that
  stores the data for the source.
* It must have an attribute matching the name of the accessor that can be used to
  set and retrieve and the value.
* When any change is made to the value, a ``change`` notification will be emitted.

Reference
---------

.. autoclass:: toga.sources.ValueSource
