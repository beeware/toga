{{ component_header("Divider", width=300) }}

## Usage

A Divider can be used to distinguish two sections of content in a layout.

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
