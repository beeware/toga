{{ component_header("ScrollContainer", width=450) }}

## Usage

```python
import toga

content = toga.Box(children=[...])

container = toga.ScrollContainer(content=content)
```

## Notes

- On Linux, ScrollContainer is supported with both GTK 3 and GTK 4, including GTK 4 with libadwaita.

## Reference

::: toga.ScrollContainer

::: toga.widgets.scrollcontainer.OnScrollHandler
