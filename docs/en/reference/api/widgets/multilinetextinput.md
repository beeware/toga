{{ component_header("MultilineTextInput", width=300) }}

## Usage

```python
import toga

textbox = toga.MultilineTextInput()
textbox.value = "Some text.\nIt can be multiple lines of text."
```

The input can be provided a placeholder value - this is a value that will be displayed to the user as a prompt for appropriate content for the widget. This placeholder will only be displayed if the widget has no content; as soon as a value is provided (either by the user, or programmatically), the placeholder content will be hidden.

## Notes

- Winforms does not support the use of partially or fully transparent colors for the MultilineTextInput background. If a color with an alpha value is provided (including `TRANSPARENT`), the alpha channel will be ignored. A `TRANSPARENT` background will be rendered as white.

## Reference

::: toga.MultilineTextInput

::: toga.widgets.multilinetextinput.OnChangeHandler
