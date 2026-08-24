{{ component_header("Widget") }}

## Usage

This class exists only for actual widgets to inherit from; it should not be be instantiated directly.

Every widget has a `style` object that controls its layout and presentation. By default, this is a [`Pack`][toga.style.Pack] style. Style properties can be set in any of these equivalent ways:

```python
import toga
from toga.style import Pack

# Provide a style object.
widget = toga.Label("Hello", style=Pack(margin=10))

# Provide style properties as constructor keyword arguments.
widget = toga.Label("Hello", margin=10)

# Read or write a style property directly on the widget.
widget.margin = 10
assert widget.margin == widget.style.margin
```

When both a `style` object and style keyword arguments are provided, the keyword arguments override matching properties from the style object. See the [Pack reference][toga.style.Pack] for the available default style properties.

## Reference

<!-- REMOVE WHEN RESOLVED -->
<!-- rumdl-disable MD013 -->
::: toga.Widget
    options:
        show_bases: false
        show_if_no_docstring: true
<!-- rumdl-enable MD013 -->

::: toga.widgets.base.StyleT
