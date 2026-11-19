{{ component_header("NumberInput", width=300) }}

## Usage

```python
import toga

widget = toga.NumberInput(min=1, max=10, step=0.001)
widget.value = 2.718
```

NumberInput's properties can accept [`Decimal`][decimal], [`int`][], [`float`][], or [`str`][] containing numbers, but they always return [`Decimal`][decimal] objects to ensure precision is retained.

## Notes

- On Linux, NumberInput is supported with both GTK 3 and GTK 4, including GTK 4 with libadwaita.

## Reference

::: toga.NumberInput

::: toga.widgets.numberinput.OnChangeHandler

::: toga.widgets.numberinput.NumberInputT
