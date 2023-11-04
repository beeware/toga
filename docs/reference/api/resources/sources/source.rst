Source
======

A base class for data source implementations.

Usage
-----

Data sources are abstractions that allow you to define the data being managed by your
application independent of the GUI representation of that data. For details on the use
of data sources, see the :doc:`background guide </background/topics/data-sources>`.

Source isn't useful on its own; it is a base class for data source implementations. It
is used by ListSource, TreeSource and ValueSource, but it can also be used by custom
data source implementations. It provides an implementation of the notification API that
data sources must provide.

Reference
---------

.. autoclass:: toga.sources.Listener

.. autoclass:: toga.sources.Source
