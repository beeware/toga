TreeSource
==========

A data source describing an ordered hierarchical tree of values.

Usage
-----

Data sources are abstractions that allow you to define the data being managed by your
application independent of the GUI representation of that data. For details on the use
of data sources, see the :doc:`background guide </background/topics/data-sources>`.

TreeSource is an implementation of an ordered hierarchical tree of values. Each node in
the tree can have children; those children can in turn have their own children.

Custom TreeSources
------------------

Any object that adheres to the TreeSource interface can be used as a data source.
Tree data sources must provide the following methods:

* ``__len__(self)`` - returns the number of root nodes in the tree

* ``__getitem__(self, index)`` - returns the root node at position ``index`` of the
  tree.

Each node returned by the Tree source is required to expose attributes matching the
accessors for any widget using the source. The node is also required to implement the
following methods:

* ``__len__(self)`` - returns the number of children of the node.

* ``__getitem__(self, index)`` - returns the child at position ``index`` of the node.

* ``can_have_children(self)`` - returns True if the node is allowed to have children.
  The result of this method does *not* depend on whether the node actually has any
  children; it only describes whether it is allowed to store children.


Reference
---------

.. autoclass:: toga.sources.Node
   :members:
   :undoc-members:

.. autoclass:: toga.sources.TreeSource
   :members:
   :undoc-members:
