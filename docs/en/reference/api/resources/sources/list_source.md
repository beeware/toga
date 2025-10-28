# ListSource

A data source describing an ordered list of data.

## Usage

Data sources are abstractions that allow you to define the data being managed by your application independent of the GUI representation of that data. For details on the use of data sources, see the [topic guide][data-sources].

ListSource is an implementation of an ordered list of data. When a ListSource is created, it is given a list of `accessors` - these are the attributes that all items managed by the ListSource will have. The API provided by ListSource is [`list`][]-like; the operations you'd expect on a normal Python list, such as `insert`, `remove`, `index`, and indexing with `[]`, are also possible on a ListSource:

```python
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

# Find an item with a name of "Thylacine"
item = source.find({"name": "Thylacine"})

# Remove that item from the data
source.remove(item)

# Insert a new item at the start of the data
source.insert(0, {"name": "Bettong", "weight": 1.2})
```

[](){ #listsource-item }

The ListSource manages a list of [`Row`][toga.sources.Row] objects. Each Row has all the attributes described by the source's `accessors`. A Row object will be constructed for each item that is added to the ListSource, and each item can be:

- A dictionary, with the accessors mapping to the keys in the dictionary.
- Any other iterable object (except for a string), with the accessors being mapped onto the items in the iterable in order of definition.
- Any other object, which will be mapped onto the *first* accessor.

Although Toga provides ListSource, you are not required to create one directly. A ListSource will be transparently constructed if you provide an iterable object to a GUI widget that displays list-like data (i.e., [`toga.Table`][], [`toga.Selection`][], or [`toga.DetailedList`][]).

## Custom List Sources

For more complex applications, you can replace ListSource with a [custom data source][custom-data-sources] class. Such a class must:

- Inherit from [`Source`][toga.sources.Source]
- Provide the same methods as [`ListSource`][toga.sources.ListSource]
- Return items whose attributes match the accessors expected by the widget
- Generate a `change` notification when any of those attributes change
- Generate `insert`, `remove` and `clear` notifications when items are added or removed

### API contract

A custom *list* source must implement *all* the public methods that list-based widgets depend on:

- `__len__(self) -> int` – total number of rows.
- `__getitem__(self, index: int | slice) -> toga.sources.Row | list[toga.sources.Row]` – random access retrieval (int returns a single `Row`; slice returns a `list[Row]`).
- `__setitem__(self, index: int, data: object) -> None` – replace an existing row (emits an `insert` notification in the built-in implementation).
- `__delitem__(self, index: int) -> None` – delete by index (emits a `remove` notification).
- `insert(self, index: int, data: object) -> toga.sources.Row` – insert a new row and return it.
- `append(self, data: object) -> toga.sources.Row` – convenience wrapper for `insert(len(self), data)`.
- `remove(self, row: toga.sources.Row) -> None` – delete an existing row instance.
- `clear(self) -> None` – remove *all* rows.
- `index(self, row: toga.sources.Row) -> int` – locate a row instance.

Implementations are free to expose additional helpers (for example, `find()` or slicing support) but the methods above constitute the **minimum contract** expected by [`toga.Table`][], [`toga.DetailedList`][] and related widgets.

### Notifications

After mutating its data the source **must** call `self.notify()` with one of the following message names so that connected widgets can refresh:

- `insert` — kwargs: `index` (*int*), `item` (*Row*). Sent after a row is inserted *or replaced*.
- `remove` — kwargs: `index` (*int*), `item` (*Row*). Sent after a row is removed.
- `change` — kwargs: `item` (*Row*). Sent when any public attribute on a row object changes.
- `clear` — *(no kwargs)*. Sent after the source becomes empty.

Omitting these notifications will leave the UI components out of sync with the underlying data.

## Reference

::: toga.sources.Row

::: toga.sources.ListSource

::: toga.sources.ListSourceT
