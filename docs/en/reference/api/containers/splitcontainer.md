# SplitContainer

A container that divides an area into two panels with a movable border.

/// tab | macOS

![/reference/images/splitcontainer-cocoa.png](/reference/images/splitcontainer-cocoa.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (GTK)

![/reference/images/splitcontainer-gtk.png](/reference/images/splitcontainer-gtk.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux (Qt) {{ not_supported }}

Not supported

///

/// tab | Windows

![/reference/images/splitcontainer-winforms.png](/reference/images/splitcontainer-winforms.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android {{ not_supported }}

Not supported

///

/// tab | iOS {{ not_supported }}

Not supported

///

/// tab | Web {{ not_supported }}

Not supported

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

```python
import toga

left_container = toga.Box()
right_container = toga.ScrollContainer()

split = toga.SplitContainer(content=[left_container, right_container])
```

Content can be specified when creating the widget, or after creation by assigning the `content` attribute. The direction of the split can also be configured, either at time of creation, or by setting the `direction` attribute:

```python
import toga
from toga.constants import Direction

split = toga.SplitContainer(direction=Direction.HORIZONTAL)

left_container = toga.Box()
right_container = toga.ScrollContainer()

split.content = [left_container, right_container]
```

By default, the space of the SplitContainer will be evenly divided between the two panels. To specify an uneven split, you can provide a flex value when specifying content. In the following example, there will be a 60/40 split between the left and right panels.

```python
import toga

split = toga.SplitContainer()
left_container = toga.Box()
right_container = toga.ScrollContainer()

split.content = [(left_container, 3), (right_container, 2)]
```

This only specifies the initial split; the split can be modified by the user once it is displayed.

## Reference

::: toga.SplitContainer

::: toga.widgets.splitcontainer.SplitContainerContentT
