{{ component_header("ScrollContainer", width=450) }}

## Usage

```python
import toga

content = toga.Box(children=[...])

container = toga.ScrollContainer(content=content)
```

## Notes

- On iOS, the system automatically pads the ScrollContainer in its scrollable directions such that the edges of the content is scrollable to the "safe area" of the container, i.e. the area of the screen not covered by system bars or partially obscured by device notches.
- On iOS versions 18 and below, ScrollContainers that are the root of the window container will be able to automatically extend into the system bars area in its scrollable directions when it reaches the edges of the containers, where the "scrolled out" portions of the containers will be covered by the system effects.
- On iOS versions 26 and above, the above happens for all ScrollContainers reaching the edges of the containers.

## Reference

::: toga.ScrollContainer

::: toga.widgets.scrollcontainer.OnScrollHandler
