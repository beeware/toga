# Table

A widget for displaying columns of tabular data. Scroll bars will be
provided if necessary.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/table-cocoa.png" width="450"
alt="/reference/images/table-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/table-gtk.png" width="450"
alt="/reference/images/table-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/table-winforms.png" width="450"
alt="/reference/images/table-winforms.png" />
</figure>
:::

::: {.group-tab}
Android [\|beta\|](##SUBST##|beta|)

<figure class="align-center">
<img src="/reference/images/table-android.png" width="450"
alt="/reference/images/table-android.png" />
</figure>
:::

::: {.group-tab}
iOS [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
Web [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

The simplest way to create a Table is to pass a list of tuples
containing the items to display, and a list of column headings. The
values in the tuples will then be mapped sequentially to the columns.

In this example, we will display a table of 2 columns, with 3 initial
rows of data:

``` python
import toga

table = toga.Table(
    headings=["Name", "Age"],
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

You can also specify data for a Table using a list of dictionaries. This
allows you to store data in the data source that won't be displayed in
the table. It also allows you to control the display order of columns
independent of the storage of that data.

``` python
import toga

table = toga.Table(
    headings=["Name", "Age"],
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

The attribute names used on each row (called "accessors") are created
automatically from the headings, by:

1.  Converting the heading to lower case
2.  Removing any character that can't be used in a Python identifier
3.  Replacing all whitespace with `_`
4.  Prepending `_` if the first character is a digit

If you want to use different attributes, you can override them by
providing an `accessors` argument. In this example, the table will use
"Name" as the visible header, but internally, the attribute "character"
will be used:

``` python
import toga

table = toga.Table(
    headings=["Name", "Age"],
    accessors={"Name", 'character'},
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

The value provided by an accessor is interpreted as follows:

- If the value is a `Widget`{.interpreted-text role="any"}, that widget
  will be displayed in the cell. Note that this is currently a beta API:
  see the Notes section.
- If the value is a `tuple`{.interpreted-text role="any"}, it must have
  two elements: an icon, and a second element which will be interpreted
  as one of the options below.
- If the value is `None`, then `missing_value` will be displayed.
- Any other value will be converted into a string. If an icon has not
  already been provided in a tuple, it can also be provided using the
  value's `icon` attribute.

Icon values must either be an `Icon`{.interpreted-text role="any"},
which will be displayed on the left of the cell, or `None` to display no
icon.

## Notes

- Widgets in cells is a beta API which may change in future, and is
  currently only supported on macOS.
- macOS does not support changing the font used to render table content.
- On Winforms, icons are only supported in the first column. On Android,
  icons are not supported at all.
- The Android implementation is [not
  scalable](https://github.com/beeware/toga/issues/1392) beyond about
  1,000 cells.

## Reference

::: {.autoclass}
toga.Table
:::

::: {.autoprotocol}
toga.widgets.table.OnSelectHandler
:::

::: {.autoprotocol}
toga.widgets.table.OnActivateHandler
:::
