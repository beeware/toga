============
Data Sources
============

Most widgets in a user interface will need to interact with data - either displaying it,
or providing a way to manipulate it.

Well designed GUI applications will maintain a strong separation between the storage and
manipulation of data, and how that data is displayed. This separation allows developers
to radically change how data is visualized without changing the underlying interface for
interacting with this data.

Toga encourages this separation through the use of data sources. Instead of directly
telling a widget to display a particular value (or collection of values), you should
define a **data source**, and then attach a widget to that source. The data source is
responsible for tracking the data that is in the source; the widget responds to those
changes in the data, providing an appropriate visualization.

Built-in data sources
=====================

There are three built-in data source types in Toga:

* :doc:`Value Sources </reference/api/resources/sources/value_source>`: For managing a single
  value. A ValueSource has a single attribute, (by default, ``value``), which is what will be
  rendered for display purposes.

* :doc:`List Sources </reference/api/resources/sources/list_source>`: For managing a list of
  items, each of which has one or more values. List data sources support the data
  manipulation methods you'd expect of a :any:`list`, and return
  :class:`~toga.sources.Row` objects. The attributes of each :class:`~toga.sources.Row`
  object are the values that should be displayed.

* :doc:`Tree Sources </reference/api/resources/sources/tree_source>`: For managing a
  hierarchy of items, each of which has one or more values. Tree data sources also
  behave like a :any:`list`, except that each item returned is a
  :class:`~toga.sources.Node`. The attributes of the :class:`~toga.sources.Node` are the
  values that should be displayed; a :class:`~toga.sources.Node` also has children,
  accessible using the :any:`list` interface on the :class:`~toga.sources.Node`.

Although Toga provides these built-in data sources, in general, *you shouldn't use them
directly*. Toga's data sources are wrappers around Python's primitive collection types -
:any:`list`, :any:`dict`, and so on. While this is useful for quick demonstrations, or
to visualize simple data, more complex applications should define their own :ref:`custom
data sources <custom-data-sources>`.

Listeners
---------

Data sources communicate using a :class:`~toga.sources.Listener` interface. When any
significant event occurs to the data source, all listeners will be notified. This
includes:

* Adding a new item
* Removing an existing item
* Changing an attribute of an existing item
* Clearing an entire data source

If any attribute of a :class:`~toga.sources.ValueSource`, :class:`~toga.sources.Row` or
:class:`~toga.sources.Node` is modified, the source will generate a change event.

When you create a widget like Selection or Table, and provide a data source for that
widget, the widget is automatically added as a listener on that source.

Although widgets are the obvious listeners for a data source, *any* object can register
as a listener. For example, a second data source might register as a listener to an
initial source to implement a filtered source. When an item is added to the first data
source, the second data source will be notified, and can choose whether to include the
new item in it's own data representation.

.. _custom-data-sources:

Custom data sources
===================

A custom data source enables you to provide a data manipulation API that makes sense for
your application. For example, if you were writing an application to display files on a
file system, you shouldn't just build a dictionary of files, and use that to construct a
:class:`~toga.sources.TreeSource`. Instead, you should write your own
``FileSystemSource`` that reflects the files on the file system. Your file system data
source doesn't need to expose ``insert()`` or ``remove()`` methods - because the end
user doesn't need an interface to "insert" files into your file system. However, you
might have a ``create_empty_file()`` method that creates a new file in the file system
and adds a representation to the data tree.

Custom data sources are also required to emit notifications whenever notable events
occur. This allows the widgets rendering the data source to respond to changes in data.
If a data source doesn't emit notifications, widgets may not reflect changes in data.
Toga provides a :doc:`Source </reference/api/resources/sources/source>` base class for
custom data source implementations. This base class implements the notification API.
