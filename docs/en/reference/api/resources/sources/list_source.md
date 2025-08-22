# ListSource

A data source describing an ordered list of data.

## Usage

Data sources are abstractions that allow you to define the data being
managed by your application independent of the GUI representation of
that data. For details on the use of data sources, see the
`topic guide </topics/data-sources>`{.interpreted-text role="doc"}.

ListSource is an implementation of an ordered list of data. When a
ListSource is created, it is given a list of `accessors` - these are the
attributes that all items managed by the ListSource will have. The API
provided by ListSource is `list`{.interpreted-text role="any"}-like; the
operations you'd expect on a normal Python list, such as `insert`,
`remove`, `index`, and indexing with `[]`, are also possible on a
ListSource:

``` python
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

::: {#listsource-item}
The ListSource manages a list of `~toga.sources.Row`{.interpreted-text
role="class"} objects. Each Row has all the attributes described by the
source's `accessors`. A Row object will be constructed for each item
that is added to the ListSource, and each item can be:
:::

- A dictionary, with the accessors mapping to the keys in the
  dictionary.
- Any other iterable object (except for a string), with the accessors
  being mapped onto the items in the iterable in order of definition.
- Any other object, which will be mapped onto the *first* accessor.

Although Toga provides ListSource, you are not required to create one
directly. A ListSource will be transparently constructed if you provide
an iterable object to a GUI widget that displays list-like data (i.e.,
`toga.Table`{.interpreted-text role="class"},
`toga.Selection`{.interpreted-text role="class"}, or
`toga.DetailedList`{.interpreted-text role="class"}).

## Custom List Sources

For more complex applications, you can replace ListSource with a
`custom data
source <custom-data-sources>`{.interpreted-text role="ref"} class. Such
a class must:

- Inherit from `Source`{.interpreted-text role="any"}
- Provide the same methods as `ListSource`{.interpreted-text role="any"}
- Return items whose attributes match the accessors expected by the
  widget
- Generate a `change` notification when any of those attributes change
- Generate `insert`, `remove` and `clear` notifications when items are
  added or removed

## Reference

::: {.autoclass special-members="__setattr__"}
toga.sources.Row
:::

::: {.autoclass special-members="__len__, __getitem__, __setitem__, __delitem__"}
toga.sources.ListSource
:::
