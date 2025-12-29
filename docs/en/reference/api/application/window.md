{{ component_header("Window", width=300) }}

## Usage

A window is the top-level container that the operating system uses to display widgets. On desktop platforms, an instance of [`Window`][toga.Window] will have a title bar, but will not have a menu or toolbar. On mobile, web and console platforms, [`Window`][toga.Window] is a bare container with no other decoration. Subclasses of [`Window`][toga.Window] (such as [`MainWindow`][toga.MainWindow]) add other decorations.

When first created, a window is not visible. To display it, call the [`show()`][toga.Window.show] method. The title of the window will default to the formal name of the app.

The window has content, which will usually be a container widget of some kind. The content of the window can be changed by re-assigning its `content` attribute to a different widget.

```python
import toga

window = toga.Window()
window.content = toga.Box(children=[...])
window.show()

# Change the window's content to something new
window.content = toga.Box(children=[...])
```

If the user attempts to close the window, Toga will call the `on_close` handler. This handler must return a `bool` confirming whether the close is permitted. This can be used to implement protections against closing a window with unsaved changes.

Once a window has been closed (either by user action, or programmatically with [`close()`][toga.Window.close]), it *cannot* be reused. The behavior of any method on a [`Window`][toga.Window] instance after it has been closed is undefined.

## Notes

- The operating system may provide controls that allow the user to resize, reposition, minimize, maximize or close the window. However, the availability of these controls is entirely operating system dependent.
- While Toga provides methods for specifying the size and position of windows, these are ultimately at the discretion of the OS (or window manager). For example, on macOS, depending on a user's OS-level settings, new windows may open as tabs on the main window; on Linux, some window managers (e.g., tiling window managers) may not honor an app's size and position requests. You should avoid making UI design decisions that are dependent on specific size and placement of windows.
- A mobile application can only have a single window (the [`main_window`][toga.App.main_window]), and that window cannot be moved, resized, or hidden. Toga will raise an exception if you attempt to create a secondary window on a mobile platform. If you try to modify the size, position, or visibility of the main window, the request will be ignored.
- On mobile platforms, a window's state cannot be [`WindowState.MINIMIZED`][toga.constants.WindowState.MINIMIZED] or [`WindowState.MAXIMIZED`][toga.constants.WindowState.MAXIMIZED]. Any request to move to these states will be ignored.
- On Linux, when using Wayland, a request to put a window into a [`WindowState.MINIMIZED`][toga.constants.WindowState.MINIMIZED] state, or to restore from the [`WindowState.MINIMIZED`][toga.constants.WindowState.MINIMIZED] state, will be ignored, and any associated events like [`on_hide()`][toga.Window.on_hide] and [`on_show()`][toga.Window.on_show], will not be triggered. This is due to limitations in window management features that Wayland allows apps to use.

## Reference

::: toga.Window

::: toga.app.WindowSet

::: toga.window.Dialog

::: toga.window.OnCloseHandler

::: toga.window.DialogResultHandler
