{{ component_header("Slider", width=300) }}

## Usage

The range is shown as a horizontal line, and the selected value is shown as a draggable marker.

A slider can either be continuous (allowing any value within the range), or discrete (allowing a fixed number of equally-spaced values). For example:

```python
import toga

def my_callback(slider):
    print(slider.value)

# Continuous slider, with an event handler.
toga.Slider(min=-5, max=10, value=7, on_change=my_callback)

# Discrete slider, accepting the values [0, 1.5, 3, 4.5, 6, 7.5].
toga.Slider(min=0, max=7.5, tick_count=6)
```

## Reference

::: toga.Slider

::: toga.widgets.slider.OnChangeHandler

::: toga.widgets.slider.OnPressHandler

::: toga.widgets.slider.OnReleaseHandler
