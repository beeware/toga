# MainWindow

A window that can use the full set of window-level user interface elements.

/// tab | macOS

![/reference/images/mainwindow-cocoa.png](/reference/images/mainwindow-cocoa.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Linux

![/reference/images/mainwindow-gtk.png](/reference/images/mainwindow-gtk.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/mainwindow-winforms.png](/reference/images/mainwindow-winforms.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android

![/reference/images/mainwindow-android.png](/reference/images/mainwindow-android.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | iOS

![/reference/images/mainwindow-iOS.png](/reference/images/mainwindow-iOS.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Web {{ beta_support }}

Screenshot not available

///

/// tab | Textual {{ beta_support }}

Screenshot not available

///

## Usage

A [`toga.MainWindow`][] is a [`toga.Window`][] that can serve as the main interface to an application. A [`toga.MainWindow`][] may optionally have a toolbar. The presentation of [`toga.MainWindow`][] is platform dependent:

- On desktop platforms that place menus inside windows (e.g., Windows, and most Linux window managers), a [`toga.MainWindow`][] instance will display a menu bar that contains the defined app [`commands`][toga.App.commands].
- On desktop platforms that use an app-level menu bar (e.g., macOS, and some Linux window managers), the window will not have a menu bar; all menu items will be displayed in the app bar.
- On mobile, web and console platforms, a [`toga.MainWindow`][] will include a title bar that can contain both menus and toolbar items.

Toolbar items can be added by adding them to [`toolbar`][toga.MainWindow.toolbar]; any command added to the toolbar will be automatically added to the App's commands as well.

```python
import toga

main_window = toga.MainWindow(title='My Application')

self.toga.App.main_window = main_window
main_window.show()
```

## Reference

::: toga.MainWindow
