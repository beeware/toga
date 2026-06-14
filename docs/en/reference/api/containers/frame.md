{{ component_header("Frame") }}

## Usage

A `Frame` is a container that visually groups its content using the platform's native grouping idiom — an `NSBox` on macOS, a `GtkFrame` on GTK, a group box on Windows, or a `MaterialCardView` on Android. The exact appearance is determined by the platform style guide and is not configurable.

```python
import toga

content = toga.Box(children=[...])

frame = toga.Frame(content=content)
```

A frame can also display a title:

```python
frame = toga.Frame(content=content, title="Details")
```

## Reference

::: toga.Frame
