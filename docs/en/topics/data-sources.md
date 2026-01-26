# Data Sources

Most widgets in a user interface will need to interact with data - either displaying it, or providing a way to manipulate it.

Well-designed GUI applications will maintain a strong separation between the storage and manipulation of data, and how that data is displayed. This separation allows developers to radically change how data is visualized without changing the underlying interface for interacting with this data.

Toga encourages this separation through the use of data sources. Instead of directly telling a widget to display a particular value (or collection of values), you should define a **data source**, and then attach a widget to that source. The data source is responsible for tracking the data that is in the source; the widget responds to those changes in the data, providing an appropriate visualization.

## Built-in data sources

There are three built-in data source types in Toga:

- [`Value Source`](/reference/api/data-representation/valuesource.md): For managing a single value. A ValueSource has a single attribute, (by default, `value`), which is what will be rendered for display purposes.
- [`List Source`](/reference/api/data-representation/listsource.md): For managing a list of items, each of which has one or more values. List data sources support the data manipulation methods you'd expect of a [`list`][], and return [`Row`][toga.sources.Row] objects. The attributes of each [`Row`][toga.sources.Row] object are the values that should be displayed.
- [`Tree Source`](/reference/api/data-representation/treesource.md): For managing a hierarchy of items, each of which has one or more values. Tree data sources also behave like a [`list`][], except that each item returned is a [`Node`][toga.sources.Node]. The attributes of the [`Node`][toga.sources.Node] are the values that should be displayed; a [`Node`][toga.sources.Node] also has children, accessible using the [`list`][] interface on the [`Node`][toga.sources.Node].

Although Toga provides these built-in data sources, in general, *you shouldn't use them directly*. Toga's data sources are wrappers around Python's primitive collection types -[`list`][], [`dict`][], and so on. While this is useful for quick demonstrations, or to visualize simple data, more complex applications should define their own [custom data sources][custom-data-sources].

### Listeners

Data sources communicate using a `Listener` interface which specifies the methods a listener object should implement to handle particular change notifications. Each type of Source has a corresponding Listener interface: [`ValueListener`][toga.sources.ValueListener], [`ListListener`][toga.sources.ListListener] and [`TreeListener`][toga.sources.TreeListener].

When any significant event occurs to the data source, all listeners will be notified. This includes:

- Adding a new item
- Removing an existing item
- Changing an attribute of an existing item
- Clearing an entire data source

If any attribute of a [`ValueSource`][toga.sources.ValueSource], [`Row`][toga.sources.Row] or [`Node`][toga.sources.Node] is modified, the source will generate a change event.

When you create a widget like Selection or Table, and provide a data source for that widget, the widget is automatically added as a listener on that source.

Although widgets are the obvious listeners for a data source, *any* object can register as a listener. For example, a second data source might register as a listener to an initial source to implement a filtered source. When an item is added to the first data source, the second data source will be notified, and can choose whether to include the new item in its own data representation. Listeners only have to implement the methods that they need for their functionality. Missing methods will be ignored.

You can add a listener by calling the [`add_listener`][toga.sources.base.Source.add_listener] method with your listener object. The standard data sources based off of the [`Source`][toga.sources.base.Source] class hold references to all their listeners and will continue to notify the listener as long as the data source remains in memory. When a listener is finished listening to a data source, you should call [`remove_listener`][toga.sources.base.Source.remove_listener] to remove the listener from the source.

This is particularly important if you might change the source that the listener is listening to. When you change data source you should make sure that you remove from the old one and connect to the new one:

``` python
class DataSourceListener:
    ...
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        # disconnect as a listener on the old data source
        self._data.remove_listener(self)
        # store a reference to the new data source
        self._data = data
        # register as a listener on the new data source
        self._data.add_listener(self)
```

If you don't disconnect, then your listener will get notifications from *both* data sources.

Often the lifetimes of data sources are closely tied to the listeners and widgets which use them, but sometimes — particularly for custom data sources — the data source may live for a long time. In these cases you should make sure that you disconnect widgets and listeners from the data source when you no longer need them. To disconnect a widget from a source, set its [`data`][toga.widgets.table.Table.data] property to `None` (or its [`items`][toga.widgets.selection.Selection.items] to `None` for a [`Selection`][toga.widgets.selection.Selection] widget). For other listeners, call [`remove_listener`][toga.sources.base.Source.remove_listener] directly. This will improve performance, and prevent delays in garbage collection of objects that your application is no longer using.

## Custom data sources

A custom data source enables you to provide a data manipulation API that makes sense for your application. For example, if you were writing an application to display files on a file system, you shouldn't just build a dictionary of files, and use that to construct a [`TreeSource`][toga.sources.TreeSource]. Instead, you should write your own `FileSystemSource` that reflects the files on the file system. Your file system data source doesn't need to expose `insert()` or `remove()` methods - because the end user doesn't need an interface to "insert" files into your file system. However, you might have a `create_empty_file()` method that creates a new file in the file system and adds a representation to the data tree.

Custom data sources are also required to emit notifications whenever notable events occur. This allows the widgets rendering the data source to respond to changes in data. To be used as a data source for a particular widget type, the custom data source must emit compatible notifications. If a data source doesn't emit notifications, widgets may not reflect changes in data. Toga provides a [`Source`][toga.sources.Source] base class for custom data source implementations. This base class implements the notification API.
