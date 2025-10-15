# Selection

A widget to select a single option from a list of alternatives.

/// tab | macOS

![/reference/images/selection-cocoa.png](/reference/images/selection-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | GTK

![/reference/images/selection-gtk.png](/reference/images/selection-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Qt {{ not_supported }}

Not supported

///

/// tab | Windows

![/reference/images/selection-winforms.png](/reference/images/selection-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/selection-android.png](/reference/images/selection-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/selection-iOS.png](/reference/images/selection-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web

![/reference/images/selection-web.png](/reference/images/selection-web.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

The Selection uses a [`ListSource`][toga.sources.ListSource] to manage the list of options. If `items` is not specified as a ListSource, it will be converted into a ListSource at runtime.

The simplest instantiation of a Selection is to use a list of strings. If a list of non-string objects are provided, they will be converted into a string for display purposes, but the original data type will be retained when returning the current value. If the string value contains newlines, only the substring up to the first newline will be displayed.

```python
import toga

selection = toga.Selection(items=["Alice", "Bob", "Charlie"])

# Change the selection to "Charlie"
selection.value = "Charlie"

# Which item is currently selected? This will print "Charlie"
print(f"Currently selected: {selection.value}")
```

A Selection can also be used to display a list of dictionaries, with the `accessor` detailing which attribute of the dictionary will be used for display purposes. When the current value of the widget is retrieved, a Row object will be returned; this Row object will have all the original data as attributes on the Row. In the following example, the GUI will only display the names in the list of items, but the age will be available as an attribute on the selected item.

```python
import toga

selection = toga.Selection(
    items=[
        {"name": "Alice", "age": 37},
        {"name": "Bob", "age": 42},
        {"name": "Charlie", "age": 24},
    ],
    accessor="name",
)

# Select Bob explicitly
selection.value = selection.items[1]

# What is the age of the currently selected person? This will print 42
print(f"Age of currently selected person: {selection.value.age}")

# Select Charlie by searching
selection.value = selection.items.find(name="Charlie")
```

## Notes

- On macOS and Android, you cannot change the font of a Selection.
- On macOS, GTK and Android, you cannot change the text color, background color, or text alignment of labels in a Selection.
- On GTK, a Selection widget with flexible sizing will expand its width (to the extent possible) to accommodate any changes in content (for example, to accommodate a long label). However, if the content subsequently *decreases* in width, the Selection widget *will not* shrink. It will retain the size necessary to accommodate the longest label it has historically contained.
- On iOS, the size of the Selection widget does not adapt to the size of the currently displayed content, or the potential list of options.

## Reference

::: toga.Selection
