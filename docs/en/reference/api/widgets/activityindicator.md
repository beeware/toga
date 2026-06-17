{{ component_header("ActivityIndicator", width=100) }}

## Usage

On most platforms, an `ActivityIndicator` is usually rendered as a "spinner".

```python
import toga

indicator = toga.ActivityIndicator()

# Start the animation
indicator.start()

# Stop the animation
indicator.stop()
```

## Notes

- The `ActivityIndicator` will always take up a fixed amount of physical space in a layout. However, the widget will not be visible when it is in a "stopped" state.

## Reference

::: toga.ActivityIndicator
