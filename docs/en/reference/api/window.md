# Window

An operating system-managed container of widgets.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/window-cocoa.png" width="300"
alt="/reference/images/window-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/window-gtk.png" width="300"
alt="/reference/images/window-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/window-winforms.png" width="300"
alt="/reference/images/window-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/window-android.png" width="300"
alt="/reference/images/window-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/window-iOS.png" width="300"
alt="/reference/images/window-iOS.png" />
</figure>
:::

::: {.group-tab}
Web

Screenshot not available
:::

::: {.group-tab}
Textual

Screenshot not available
:::
::::::::::

## Usage

A window is the top-level container that the operating system uses to
display widgets. On desktop platforms, an instance of
`~toga.Window`{.interpreted-text role="class"} will have a title bar,
but will not have a menu or toolbar. On mobile, web and console
platforms, `~toga.Window`{.interpreted-text role="class"} is a bare
container with no other decoration. Subclasses of
`~toga.Window`{.interpreted-text role="class"} (such as
`~toga.MainWindow`{.interpreted-text role="class"}) add other
decorations.

When first created, a window is not visible. To display it, call the
`~toga.Window.show`{.interpreted-text role="meth"} method. The title of
the window will default to the formal name of the app.

The window has content, which will usually be a container widget of some
kind. The content of the window can be changed by re-assigning its
`content` attribute to a different widget.

``` python
import toga

window = toga.Window()
window.content = toga.Box(children=[...])
window.show()

# Change the window's content to something new
window.content = toga.Box(children=[...])
```

If the user attempts to close the window, Toga will call the `on_close`
handler. This handler must return a `bool` confirming whether the close
is permitted. This can be used to implement protections against closing
a window with unsaved changes.

Once a window has been closed (either by user action, or
programmatically with `~toga.Window.close()`{.interpreted-text
role="meth"}), it *cannot* be reused. The behavior of any method on a
`~toga.Window`{.interpreted-text role="class"} instance after it has
been closed is undefined.

## Notes

- The operating system may provide controls that allow the user to
  resize, reposition, minimize, maximize or close the window. However,
  the availability of these controls is entirely operating system
  dependent.
- While Toga provides methods for specifying the size and position of
  windows, these are ultimately at the discretion of the OS (or window
  manager). For example, on macOS, depending on a user's OS-level
  settings, new windows may open as tabs on the main window; on Linux,
  some window managers (e.g., tiling window managers) may not honor an
  app's size and position requests. You should avoid making UI design
  decisions that are dependent on specific size and placement of
  windows.
- A mobile application can only have a single window (the
  `~toga.App.main_window`{.interpreted-text role="attr"}), and that
  window cannot be moved, resized, or hidden. Toga will raise an
  exception if you attempt to create a secondary window on a mobile
  platform. If you try to modify the size, position, or visibility of
  the main window, the request will be ignored.
- On mobile platforms, a window's state cannot be
  `WindowState.MINIMIZED`{.interpreted-text role="any"} or
  `WindowState.MAXIMIZED`{.interpreted-text role="any"}. Any request to
  move to these states will be ignored.
- On Linux, when using Wayland, a request to put a window into a
  `WindowState.MINIMIZED`{.interpreted-text role="any"} state, or to
  restore from the `WindowState.MINIMIZED`{.interpreted-text role="any"}
  state, will be ignored, and any associated events like
  `~toga.Window.on_hide`{.interpreted-text role="meth"} and
  `~toga.Window.on_show`{.interpreted-text role="meth"}, will not be
  triggered. This is due to limitations in window management features
  that Wayland allows apps to use.

## Reference

::: {.autoclass}
toga.Window
:::

::: {.autoclass}
toga.app.WindowSet
:::

::: {.autoprotocol}
toga.window.Dialog
:::

::: {.autoprotocol}
toga.window.OnCloseHandler
:::

::: {.autoprotocol}
toga.window.DialogResultHandler
:::
