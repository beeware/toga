{{ component_header("Widget") }}

## Usage

This class exists only for actual widgets to inherit from; it should not be instantiated directly.

Because `Widget` inherits from `PackMixin`, all [Pack style properties](../style/pack.md)
can be set directly on any widget instance. For example:

```python
# Instead of this:
widget.style.flex = 1

# You can write this:
widget.flex = 1
```

## Reference

<!-- REMOVE WHEN RESOLVED -->
<!-- rumdl-disable MD013 -->
::: toga.Widget
    options:
        show_if_no_docstring: true
<!-- rumdl-enable MD013 -->

::: toga.widgets.base.PackMixin

::: toga.widgets.base.StyleT
