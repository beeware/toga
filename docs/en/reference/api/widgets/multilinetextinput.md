{{ component_header("MultilineTextInput", width=300) }}

## Usage

```python
import toga

textbox = toga.MultilineTextInput()
textbox.value = "Some text.\nIt can be multiple lines of text."
```

The input can be provided a placeholder value - this is a value that will be displayed to the user as a prompt for appropriate content for the widget. This placeholder will only be displayed if the widget has no content; as soon as a value is provided (either by the user, or programmatically), the placeholder content will be hidden.

Spell checking is enabled by default where the platform supports it. Use `toga.MultilineTextInput(spell_checking=False)` to disable it, or change the `spell_checking` property after construction.

## Notes

- On Android, disabling spell checking also disables keyboard suggestions. A read-only input always disables suggestions; making it editable again restores the requested spelling setting.
- On GTK, spell checking is a hint to the input method; support depends on the input method in use.
- Qt and WinForms do not provide built-in spell checking. The setting is accepted but has no effect.
- Other text assistance, such as automatic correction and automatic capitalization, retains its platform behavior.
- WinForms does not support the use of partially or fully transparent colors for the MultilineTextInput background. If a color with an alpha value is provided (including `TRANSPARENT`), the alpha channel will be ignored. A `TRANSPARENT` background will be rendered as white.

## Reference

::: toga.MultilineTextInput

::: toga.widgets.multilinetextinput.OnChangeHandler
