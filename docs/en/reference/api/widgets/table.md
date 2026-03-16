{{ component_header("Table", width=450) }}

## Usage

The simplest way to create a Table is to pass a list of tuples containing the items to display, and a list of column headings. The values in the tuples will then be mapped sequentially to the columns.

In this example, we will display a table of 2 columns, with 3 initial rows of data:

```python
import toga

table = toga.Table(
    columns=["Name", "Age"],
    data=[
        ("Arthur Dent", 42),
        ("Ford Prefect", 37),
        ("Tricia McMillan", 38),
    ]
)

# Get the details of the first item in the data:
print(f"{table.data[0].name} is age {table.data[0].age}")

# Append new data to the table
table.data.append(("Zaphod Beeblebrox", 47))
```

You can also specify data for a Table using a list of dictionaries. This allows you to store data in the data source that won't be displayed in the table. It also allows you to control the display order of columns independent of the storage of that data.

```python
import toga

table = toga.Table(
    columns=["Name", "Age"],
    data=[
        {"name": "Arthur Dent", "age": 42, "planet": "Earth"},
        {"name": "Ford Prefect", "age": 37, "planet": "Betelgeuse Five"},
        {"name": "Tricia McMillan", "age": 38, "planet": "Earth"},
    ]
)

# Get the details of the first item in the data:
row = table.data[0]
print(f"{row.name}, who is age {row.age}, is from {row.planet}")
```

The strings for the headings are translated into [`AccessorColumn`][toga.sources.AccessorColumn] objects which tell the `Table` how to get the values to display in the column by looking up attributes on the rows.

-8<- "snippets/accessors.md"

If you want to use attributes which don't match the headings, you can override them by providing your own `AccessorColumn` objects. In this example, the table will use "Name" as the visible header, but internally, the attribute "character" will be used:

```python
import toga

table = toga.Table(
    columns=[
        AccessorColumn("Name", "character"),
        "Age",
    ],
    data=[
        {"character": "Arthur Dent", "age": 42, "planet": "Earth"},
        {"character": "Ford Prefect", "age": 37, "planet": "Betelgeuse Five"},
        {"name": "Tricia McMillan", "age": 38, "planet": "Earth"},
    ]
)

# Get the details of the first item in the data:
row = table.data[0]
print(f"{row.character}, who is age {row.age}, is from {row.planet}")
```

-8<- "snippets/accessor-values.md"

So for example:

```python
import toga

green_icon = toga.Icon("icons/green")

table = toga.Table(
    columns=["Name", "Age"],
    data=[
        ((green_icon, "Arthur Dent"), 42),
        ((None, "Ford Prefect"), 37),
        ("Tricia McMillan", 38),
    ]
)
```
will display the green icon in the first column of the first row and no other icons.

The [`AccessorColumn`][toga.sources.AccessorColumn] class is the only column class provided in core Toga, but you can define your own [custom columns](../data-representation/column.md) that implement the [`ColumnT`][toga.sources.ColumnT] protocol and there is a [`Column`][toga.sources.Column] abstract base class that serves as a useful starting point. These columns can do things like giving you better control over getting icons and text, formatting in a particular way, combining multiple attributes to produce the value to display, or even accessing data via indexes rather than attribute lookup.

Sometimes when supplying rows using lists or other sequences, the order of the columns may not match the order of the data in the rows. In this case, the easiest approach is to create a [ListSource][`toga.sources.ListSource`] that maps the rows to the column accessors:

```python
import toga

table = toga.Table(
    columns=["Age", "Name"],
    data=toga.sources.ListSource(
        accessors=["name", "planet", "age"],
        [
            ("Arthur Dent", "Earth", 42),
            ("Ford Prefect", "Betelgeuse Five", 37),
            ("Tricia McMillan", "Earth", 38),
        ],
    )
)
```

For more complex data you can define your own [custom data sources](/topics/data-sources.md).

## Notes

- Widgets in cells is a beta API which may change in future, and is currently only supported on macOS.
- macOS does not support changing the font used to render table content.
- Icons in tables are not supported on Android, and the implementation is [not scalable](https://github.com/beeware/toga/issues/1392) beyond about 1,000 cells.

## Reference

::: toga.Table

::: toga.widgets.table.OnSelectHandler

::: toga.widgets.table.OnActivateHandler
