============
Data Sources
============

Most widgets in a user interface will need to interact with data - either
displaying it, or providing a way to manipulate it.

Well designed GUI applications will maintain a strong separation between the
data, and how that data is displayed. This separation allows developers to
radically change how data is visualized without changing the underlying
interface for interacting with this data.

Toga encourages this separation by using data sources. Instead of directly
telling a widget to display a particular value (or collection of values), Toga
requires you to define a **data source**, and then tell a widget to display that
source.

Built-in data sources
=====================

There are three built-in data source types in Toga:

* **Value Sources**: For managing a single value. A ``Value`` has a single
  attribute, ``value``, which is the value that will be rendered for display
  purposes.

* **List Sources**: For managing a list of items, each of which has one or
  more values. List data sources support the data manipulation methods you'd
  expect of a ``list``, and return ``Row`` objects. The attributes of each
  ``Row`` object are the values that should be displayed.

* **Tree Sources**: For managing a heirarchy of items, each of which has one
  or more values. Tree data sources also behave like a ``list``, except that each
  item returned is a ``Node``. The attributes of the ``Node`` are the values
  that should be displayed; a ``Node`` also has children, accessible using
  the ``list`` interface on the ``Node``.

Listeners
---------

Data sources communicate to widgets (and other data sources) using a listener
interface. Once a data source has been created, any other object can register
as a listener on that data source. When any significant event occurs to the data
source, all listeners will be notified.

Notable events include:
* Adding a new item
* Removing an existing item
* Changing a value on an item
* Clearing an entire data source

If any attribute of a ``Value``, ``Row`` or ``Node`` is modified, the source
will generate a change event.

Custom data sources
===================

Although Toga provides built-in data sources, in general, *you shouldn't use
them*. Toga's data sources are wrappers around Python's primitive data
types - `int`, `str`, `list`, `dict`, and so on. While this is useful for
quick demonstrations, or to visualize simple data, more complex applications
should define their own data sources.

A custom data source enables you to provide a data manipulation API that makes
sense for your application. For example, if you were writing an application to
display files on a file system, you shouldn't just build a dictionary of
files, and use that to construct a ``TreeSource``. Instead, you should write
your own ``FileSystemSource`` that reflects the files on the file system. Your
file system data source doesn't need to expose ``insert()`` or ``remove()``
methods - because the end user doesn't need an interface to "insert" files
into your filesystem. However, you might have a `create_empty_file()` method
that creates a new file in the filesystem, and adds a representation to the
tree.

Custom data sources are also required to emit notifications whenever notable
events occur. This allows the widgets rendering the data source to respond
to changes in data. If a data source doesn't emit notifications, widgets
may not reflect changes in data.

Value sources
-------------

A Value source is any object with a "value" attribute.

List sources
------------

List data sources need to provide the following methods:

* ``__len__(self)`` - returns the number of items in the list

* ``__getitem__(self, index)`` - returns the item at position ``index`` of
  the list.

Each item returned by the List source is required to expose
attributes matching the accessors for any widget using the source.

Tree sources
------------

Tree data sources need to provide the following methods:

* ``__len__(self)`` - returns the number of root nodes in the tree

* ``__getitem__(self, index)`` - returns the root node at position ``index`` of
  the tree.

Each node returned by the Tree source is required to expose
attributes matching the accessors for any widget using the source.
The node is also required to implement the following methods:

* ``__len__(self)`` - returns the number of children of the node.

* ``__getitem__(self, index)`` - returns the child at position ``index`` of
  the node.

* ``can_have_children(self)`` - returns True if the node is allowed to have
  children. The result of this method does *not* depend on whether the
  node actually has any children; it only describes whether it is allowed
  to store children.
