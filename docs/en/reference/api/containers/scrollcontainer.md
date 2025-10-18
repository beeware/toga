# ScrollContainer

A container that can display a layout larger than the area of the container, with overflow controlled by scroll bars.

/// tab | macOS

![/reference/images/scrollcontainer-cocoa.png](/reference/images/scrollcontainer-cocoa.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux

![/reference/images/scrollcontainer-gtk.png](/reference/images/scrollcontainer-gtk.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/scrollcontainer-winforms.png](/reference/images/scrollcontainer-winforms.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/scrollcontainer-android.png](/reference/images/scrollcontainer-android.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/scrollcontainer-iOS.png](/reference/images/scrollcontainer-iOS.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web

![/reference/images/scrollcontainer-web.png](/reference/images/scrollcontainer-web.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

```python
import toga

content = toga.Box(children=[...])

container = toga.ScrollContainer(content=content)
```

## Reference

::: toga.ScrollContainer

::: toga.widgets.scrollcontainer.OnScrollHandler
