{{ component_header("ScrollContainer", width=450) }}

## Usage

```python
import toga

content = toga.Box(children=[...])

container = toga.ScrollContainer(content=content)
```

On each axis where scrolling is disabled, the minimum size of a `ScrollContainer` includes the minimum size of its content. Content size does not affect the container's minimum on an axis where scrolling is enabled.

## Reference

::: toga.ScrollContainer

::: toga.widgets.scrollcontainer.OnScrollHandler
