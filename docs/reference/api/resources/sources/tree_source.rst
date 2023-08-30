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
nodes, and also on each node within the tree.

.. code-block:: python

    from toga.sources import TreeSource

    source = TreeSource(
        accessors=["name", "height"],
        data={
            "Animals": [
                ({"name": "Numbat", "height": 0.15}, None),
                ({"name": "Thylacine", "height": 0.6}, None),
            ],
            "Plants": [
                ({"name": "Woollybush", "height": 2.4}, None),
                ({"name": "Boronia", "height": 0.9}, None),
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

The TreeSource manages a tree of :class:`~toga.sources.Node` objects. Each Node has all
the attributes described by the source's ``accessors``. A Node object will be
constructed for each item that is added to the TreeSource.

Each Node object in the TreeSource can have children; those children can in turn have
their own children. A child that *cannot* have children is called a *leaf Node*. Whether
a child *can* have children is independent of whether it *does* have children - it is
possible for a Node to have no children and *not* be a leaf node. This is analogous to
files and directories on a file system: a file is a leaf Node, as it cannot have
children; a directory *can* contain files and other directories in it, but it can also
be empty. An empty directory would *not* be a leaf Node.

.. _treesource-item:

When creating a single Node for a TreeSource (e.g., when inserting a new item), the data
for the Node can be specified as:

* A dictionary, with the accessors mapping to the keys in the dictionary

* Any iterable object (except for a string), with the accessors being mapped
  onto the items in the iterable in order of definition.

* Any other object, which will be mapped onto the *first* accessor.

When constructing an entire TreeSource, the data can be specified as:

* A dictionary. The keys of the dictionary will be converted into Nodes, and used as
  parents; the values of the dictionary will become the children of their corresponding
  parent.

* Any other iterable object (except a string). Each value in the iterable will be
  treated as a 2-item tuple, with the first item being data for the parent Node, and the
  second item being the child data.

* Any other object will be converted into a single node with no children.

When specifying children, a value of :any:`None` for the children will result in the
creation of a leaf node. Any other value will be processed recursively - so, a child
specifier can itself be a dictionary, an iterable of 2-tuples, or data for a single
child, and so on.

Although Toga provides TreeSource, you are not required to create one directly. A TreeSource
will be transparently constructed for you if you provide one of the items listed above (e.g.
:any:`list`, :any:`dict`, etc) to a GUI widget that displays tree-like data (i.e.,
:class:`toga.Tree`).

Custom TreeSources
------------------

For more complex applications, you can replace TreeSource with a :ref:`custom data
source <custom-data-sources>` class. Such a class must:

* Inherit from :any:`Source`

* Provide the same methods as :any:`TreeSource`

* Return items whose attributes match the accessors expected by the widget

* Generate a ``change`` notification when any of those attributes change

* Generate ``insert``, ``remove`` and ``clear`` notifications when nodes are added or
  removed

Reference
---------

.. autoclass:: toga.sources.Node
   :special-members: __len__, __getitem__, __setitem__, __delitem__

.. autoclass:: toga.sources.TreeSource
   :special-members: __len__, __getitem__, __setitem__, __delitem__
