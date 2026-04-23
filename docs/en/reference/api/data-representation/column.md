{{ component_header("Column") }}

## Usage

Columns are abstractions that allow you to specify how the data in a Table or Tree widget should be displayed. Each column object is responsible for taking a row from the data source and providing text, icon and other display elements suitable for the Table and Tree widgets to use.

The protocol, [`ColumnT`][toga.sources.ColumnT], describes what custom Column implementations need to provide so that they can be used by the widget. Toga provides the [`Column`][toga.sources.Column] and [`AccessorColumn`][toga.sources.AccessorColumn] as implementations of the `ColumnT` protocol. The [`Column`][toga.sources.Column] class is a base class suitable for custom sub-classing, while the [`AccessorColumn`][toga.sources.AccessorColumn] is used by default in the [`Table`][toga.widgets.table.Table] and [`Tree`][toga.widgets.tree.Tree] widgets.

Column objects are usually immutable, and can be shared between widgets freely if desired.

### Accessor columns

`AccessorColumn` objects are designed to work with the [`ListSource`][toga.sources.ListSource] and [`TreeSource`][toga.sources.TreeSource] objects: each `AccessorColumn` holds the heading text and an attribute name, or "accessor", that is used to get values from each row of the source to use in the column.

The `Table` and `Tree` widgets will automatically create `AccessorColumn` objects from column headings, but they can also be created manually if desired. Each column object expects a heading and an accessor as arguments, but will automatically generate an accessor from the heading if needed.

```python
table = Table(
    columns=[
        AccessorColumn("Title", "title"),
        AccessorColumn("Year"),
        "Rating",  # equivalent to AccessorColumn("Rating")
    ]
)
```

-8<- "snippets/accessors.md"

-8<- "snippets/accessor-values.md"

### Custom columns

You can define your own subclasses that can override the way that text and icons are computed to provide custom formatting of text. Any object which implements the [`ColumnT`][toga.sources.ColumnT] protocol can be used. This protocol requires:

- a read-only [`heading`][toga.sources.ColumnT.heading] property that is the column heding text or `None` for no heading text.;
- a [`value`][toga.sources.ColumnT.value] method that takes a row object and gives the value for the column in that row.
- a [`text`][toga.sources.ColumnT.text] method that takes a row object and an optional default value and gives the text for the column to display in that row, or `None` if no text is to be displayed.
- an [`icon`][toga.sources.ColumnT.icon] method that takes a row object and gives the icon for the column to display in that row, or `None` if no icon is to be displayed.
- a [`widget`][toga.sources.ColumnT.widget] method that takes a row object and gives the widget for the column to use in that row, or `None` if no widget is to be used (this is experimental and is only supported on macOS at present).

For example, we could subclass `AccessorColumn` to make column that takes a value which is a list of strings and formats it as a comma-separated list as follows:

```python
class ListStrColumn(AccessorColumn):

    def text(self, row, default=None):
        value = self.value(row)
        if value is None:
            return default
        else:
            return ", ".join(value)

table = Table(
    columns=[
        "Title",
        ListStrColumn("Genre"),
    ]
)
```

so a row providing the value `["Drama", "Action"]` would be displayed in the table cell as `"Drama, Action"`.

Custom columns can even override the default way of looking up values to allow such things as combining values from multiple attributes, looking up values by index rather than attribute, or using a method or function on the row to get the display values. The [`Column`][toga.sources.Column] class provides a convenient minimal base class for implementing custom columns.

```python
class TotalCostColumn(Column):

    def value(self, row):
        return row.item_cost * row.quantity

    def text(self, row, default=None):
        value = self.value(row)
        return f"${value:.2d}"

table = Table(
    columns=[
        "Product",
        "Quantity",
        "Item Cost",
        TotalCostColumn("Total Cost"),
    ]
)
```

## Reference

::: toga.sources.ColumnT

::: toga.sources.Column

::: toga.sources.AccessorColumn
