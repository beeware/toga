{{ component_header("PasswordInput", width=300) }}

## Usage

Any value typed by the user will be obscured, allowing the user to see the number of characters they have typed, but not the actual characters.

The `PasswordInput` supports the same validation and event handlers as a [`TextInput`][toga.TextInput].

```python
import toga

password = toga.PasswordInput()
```

## Notes

- WinForms does not support the use of partially or fully transparent colors for the PasswordInput background. If a color with an alpha value is provided (including `TRANSPARENT`), the alpha channel will be ignored. A `TRANSPARENT` background will be rendered as white.
- On WinForms, if a PasswordInput is given an explicit height, the rendered widget will not expand to fill that space. The widget will have the fixed height determined by the font used on the widget. In general, you should avoid setting a `height` style property on PasswordInput widgets.

## Reference

::: toga.PasswordInput
