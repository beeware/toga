{{ component_header("Tree", width=450) }}

## Usage

The simplest way to create a Tree is to pass a dictionary and a list of column headings. Each key in the dictionary can be either a tuple, whose contents will be mapped sequentially to the columns of a node, or a single object, which will be mapped to the first column. And each value in the dictionary can be either another dictionary containing the children of that node, or `None` if there are no children.

In this example, we will display a tree with 2 columns. The tree will have 2 root nodes; the first root node will have 1 child node; the second root node will have 2 children. The root nodes will only populate the "name" column; the other column will be blank:

```python
import toga

tree = toga.Tree(
    columns=["Name", "Age"],
    data={
        "Earth": {
           ("Arthur Dent", 42): None,
        },
        "Betelgeuse Five": {
           ("Ford Prefect", 37): None,
           ("Zaphod Beeblebrox", 47): None,
        },
    }
)

# Get the details of the first child of the second root node:
print(f"{tree.data[1][0].name} is age {tree.data[1][0].age}")

# Append new data to the first root node in the tree
tree.data[0].append(("Tricia McMillan", 38))
```

You can also specify data for a Tree using a list of 2-tuples, with dictionaries providing data values. This allows you to store data in the data source that won't be displayed in the tree. It also allows you to control the display order of columns independent of the storage of that data.

```python
import toga

tree = toga.Tree(
    columns=["Name", "Age"],
    data=[
        (
            {"name": "Earth"},
            [({"name": "Arthur Dent", "age": 42, "status": "Anxious"}, None)]
        ),
        (
            {"name": "Betelgeuse Five"},
            [
                ({"name": "Ford Prefect", "age": 37, "status": "Hoopy"}, None),
                ({"name": "Zaphod Beeblebrox", "age": 47, "status": "Oblivious"}, None),
            ]
        ),
    ]
)

# Get the details of the first child of the second root node:
node = tree.data[1][0]
print(f"{node.name}, who is age {node.age}, is {node.status}")
```

The strings for the headings are translated into [`AccessorColumn`][toga.sources.AccessorColumn] objects which tell the `Tree` how to get the values to display in the column by looking up attributes on the nodes.

-8<- "snippets/accessors.md"

If you want to use attributes which don't match the headings, you can override them by providing your own `AccessorColumn` objects. In this example, the table will use "Name" as the visible header, but internally, the attribute "character" will be used:

```python
import toga

tree = toga.Tree(
    columns=[AccessorColumn("Name", 'character'), "Age"],
    data=[
        (
            {"character": "Earth"},
            [({"character": "Arthur Dent", "age": 42, "status": "Anxious"}, None)]
        ),
        (
            {"character": "Betelgeuse Five"},
            [
                ({"character": "Ford Prefect", "age": 37, "status": "Hoopy"}, None),
                ({"character": "Zaphod Beeblebrox", "age": 47, "status": "Oblivious"}, None),
            ]
        ),
    ]
)

# Get the details of the first child of the second root node:
node = tree.data[1][0]
print(f"{node.character}, who is age {node.age}, is {node.status}")
```

-8<- "snippets/accessor-values.md"

So, for example:

```python
import toga

green_icon = toga.Icon("icons/green")

tree = toga.Tree(
    columns=["Name", "Age"],
    data=[
        (
            {"name": (green_icon, "Earth")},
            [({"name": "Arthur Dent", "age": 42, "status": "Anxious"}, None)]
        ),
        (
            {"name": (None, "Betelgeuse Five")},
            [
                ({"name": "Ford Prefect", "age": 37, "status": "Hoopy"}, None),
                ({"name": "Zaphod Beeblebrox", "age": 47, "status": "Oblivious"}, None),
            ]
        ),
    ]
)
```

will display a green icon next to "Earth", and nothing next to "Betelgeuse Five".

The [`AccessorColumn`][toga.sources.AccessorColumn] class is the only column class provided in core Toga, but you can define your own [custom columns](../data-representation/column.md) that implement the [`ColumnT`][toga.sources.ColumnT] protocol and there is a [`Column`][toga.sources.Column] abstract base class that serves as a useful starting point. These columns can do things like giving you better control over getting icons and text, formatting in a particular way, combining multiple attributes to produce the value to display, or even accessing data via indexes rather than attribute lookup.

Sometimes when supplying rows using lists or other sequences, the order of the columns may not match the order of the data in the rows. In this case, the easiest approach is to create a [TreeSource][`toga.sources.TreeSource`] that maps the rows to the column accessors:

```python
import toga

tree = toga.Tree(
    columns=["Age", "Name"],
    data=TreeSource(
        accessors=["name", "status", "age"]
        data={
            "Earth": {
                ("Arthur Dent", "Anxious", 42): None,
            },
            "Betelgeuse Five": {
                ("Ford Prefect", "Hoopy", 37): None,
                ("Zaphod Beeblebrox", "Oblivious", 47): None,
            },
        }
    )
)
```

For more complex data you can define your own [custom data sources](/topics/data-sources.md).

## Notes

- Widgets in cells is a beta API which may change in future, and is currently only supported on macOS.
- On macOS, you cannot change the font used in a Tree.

## Reference

::: toga.Tree

::: toga.widgets.tree.OnSelectHandler

::: toga.widgets.tree.OnActivateHandler
