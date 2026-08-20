{{ component_header("Widget") }}

## Usage

This class exists only for actual widgets to inherit from; it should not be be instantiated directly.

Because every widget inherits from `PackMixin`, all widgets support the [Pack style properties](/reference/api/style/pack.md) directly on the widget itself — for example, `widget.color` instead of `widget.style.color`. See the [Pack reference](/reference/api/style/pack.md) for the full list of properties that can be set this way.

## Reference

<!-- REMOVE WHEN RESOLVED -->
<!-- rumdl-disable MD013 -->
::: toga.Widget
    options:
        show_if_no_docstring: true
<!-- rumdl-enable MD013 -->

::: toga.widgets.base.StyleT
