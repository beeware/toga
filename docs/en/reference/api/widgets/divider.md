# Divider

A separator used to visually distinguish two sections of content in a layout.

/// tab | macOS

![/reference/images/divider-cocoa.png](/reference/images/divider-cocoa.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (GTK)

![/reference/images/divider-gtk.png](/reference/images/divider-gtk.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (Qt) {{ not_supported }}

Not supported

///

/// tab | Windows

![/reference/images/divider-winforms.png](/reference/images/divider-winforms.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/divider-android.png](/reference/images/divider-android.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/divider-iOS.png](/reference/images/divider-iOS.png){ width="300" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ beta_support }}

Screenshot not available

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

To separate two labels stacked vertically with a horizontal line:

```python
import toga
from toga.style.pack import Pack, COLUMN

box = toga.Box(
    children=[
        toga.Label("First section"),
        toga.Divider(),
        toga.Label("Second section"),
    ],
    direction=COLUMN,
    flex=1,
    margin=10
)
```

The direction (horizontal or vertical) can be given as an argument. If not specified, it will default to horizontal.

## Reference

::: toga.Divider
