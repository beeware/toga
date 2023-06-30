TreeSource
==========

A data source describing an ordered hierarchical tree of values.

Usage
-----

Data sources are abstractions that allow you to define the data being managed by your
application independent of the GUI representation of that data. For details on the use
of data sources, see the :doc:`background guide </background/topics/data-sources>`.

TreeSource is an implementation of an ordered hierarchical tree of values. When a
TreeSource is created, it is given a list of ``accessors`` - these are the attributes
that all items managed by the TreeSource will have. The API provided by TreeSource is
:any:`list`-like; the operations you'd expect on a normal Python list, such as
``insert``, ``remove``, ``index``, and indexing with ``[]``, are also possible on a
TreeSource. These methods are available on the TreeSource itself to manipulate root
nodes, and also on each item of the TreeSource to manipulate children.

.. code-block:: python

    from toga.sources import TreeSource

    source = TreeSource(
        accessors=["name", "height"],
        data={
            "Animals": [
                {"name": "Numbat", "height": 0.15},
                {"name": "Thylacine", "height": 0.6},
            ],
            "Plants": [
                {"name": "Woollybush", "height": 2.4},
                {"name": "Boronia", "height": 0.9},
            ],
        }
    )

    # Get the Animal group in the source.
    # The Animal group won't have a "height" attribute.
    group = source[0]
    print(f"Group's name is {group.name}")

    # Get the second item in the animal group
    animal = group[1]
    print(f"Animals's name is {animal.name}; it is {animal.height}m tall.")

    # Find an animal with a name of "Thylacine"
    row = source.find(parent=source[0], {"name": "Thylacine"})

    # Remove that row from the data. Even though "Thylacine" isn't a root node,
    # remove will find it and remove it from the list of animals.
    source.remove(row)

    # Insert a new item at the start of the list of animals.
    group.insert(0, {"name": "Bettong", "height": 0.35})

    # Insert a new root item in the middle of the list of root nodes
    source.insert(1, {"name": "Minerals"})

The TreeSource manages a tree of :class:`~toga.sources.Node` objects. Each Node object
in the TreeSource is an object that has all the attributes described by the
``accessors`` for the TreeSource. A Node object will be constructed by the source for
each item that is added or removed from the ListSource.

Each Node object in the TreeSource can have children; those children can in turn have
their own children. A child that *cannot* have children is called a *leaf Node*. Whether
a child *can* have children is independent of whether it *does* have children - it is
possible for a Node to have no children and *not* be a leaf node. This is analogous to
files and directories on a file system: a file is a leaf Node, as it cannot have
children; a directory *can* contain files and other directories in it, but it can also
be empty. An empty directory would *not* be a leaf Node.

When creating a single Node for a TreeSource (e.g., when inserting a new item), the data
for the Node can be specified as:

* A dictionary, with the accessors mapping to the keys in the dictionary

* Any iterable object (except for a string), with the accessors being mapped
  onto the items in the iterable in order of definition. This requires that the
  iterable object have *at least* as many values as the number of accessors
  defined on the TreeSource.

* Any other object, which will be mapped onto the *first* accessor.

When constructing an entire ListSource, the data can be specified as:

* A dictionary. The keys of the dictionary will be converted into Nodes, and used as
  parents; the values of the dictionary will become the children of their corresponding
  parent.

* Any iterable object (except a string). Each value in the iterable will be treated as
  a 2-item tuple, with first item being data for the parent Node, and the second item
  being the child data.

* Any other object. The object will be converted into a list containing a single node
  with no children.

When specifying children, a value of :any:`None` for the children will result in the
creation of a leaf node. Any other value will be processed recursively - so, a child
specifier can itself be a dictionary, an iterable of 2-tuples, or data for a single
child; each of which can specify their own children, and so on.

Although Toga provides TreeSource, you are not required to use it directly. A TreeSource
will be transparently constructed for you if you provide Python primitives (e.g.
:any:`list`, :any:`dict`, etc) to a GUI widget that displays tree-like data (i.e.,
:class:`toga.Tree`). Any object that adheres to the same interface can be used as an
alternative source of data for widgets that support using a TreeSource. See the
background guide on :ref:`custom data sources <custom-data-sources>` for more details.

Custom TreeSources
------------------

Any object that adheres to the TreeSource interface can be used as a data source. The
TreeSource, plus every node managed by the TreeSource, must provide the following
methods:

* ``__len__()`` - returns the number of children of this node, or the number of root
  nodes for the TreeSource.

* ``__getitem__(index)`` - returns the child at position ``index`` of a node, or the
  root node at position ``index`` of the TreeSource.

Every node on the TreeSource must also provide:

* ``can_have_children()`` - returns ``False`` if the node is a leaf node.

A custom TreeSource must also generate ``insert``, ``remove`` and ``clear``
notifications when items are added or removed from the source, or when children are
added or removed to nodes managed by the TreeSource.

Each node returned by the custom TreeSource is required to expose attributes matching
the accessors for any widget using the source. Any change to the values of these attributes
must generate a ``change`` notification on any listener to the custom ListSource.

Reference
---------

.. autoclass:: toga.sources.Node
   :members:
   :undoc-members:

.. autoclass:: toga.sources.TreeSource
   :members:
   :undoc-members:
