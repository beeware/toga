# MainWindow

A window that can use the full set of window-level user interface
elements.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/mainwindow-cocoa.png" width="450"
alt="/reference/images/mainwindow-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/mainwindow-gtk.png" width="450"
alt="/reference/images/mainwindow-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/mainwindow-winforms.png" width="450"
alt="/reference/images/mainwindow-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/mainwindow-android.png" width="450"
alt="/reference/images/mainwindow-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/mainwindow-iOS.png" width="450"
alt="/reference/images/mainwindow-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|beta\|](##SUBST##|beta|)

Screenshot not available
:::

::: {.group-tab}
Textual [\|beta\|](##SUBST##|beta|)

Screenshot not available
:::
::::::::::

## Usage

A `toga.MainWindow`{.interpreted-text role="class"} is a
`toga.Window`{.interpreted-text role="class"} that can serve as the main
interface to an application. A `toga.MainWindow`{.interpreted-text
role="class"} may optionally have a toolbar. The presentation of
`toga.MainWindow`{.interpreted-text role="class"} is platform dependent:

- On desktop platforms that place menus inside windows (e.g., Windows,
  and most Linux window managers), a `toga.MainWindow`{.interpreted-text
  role="class"} instance will display a menu bar that contains the
  defined app `~toga.App.commands`{.interpreted-text role="attr"}.
- On desktop platforms that use an app-level menu bar (e.g., macOS, and
  some Linux window managers), the window will not have a menu bar; all
  menu items will be displayed in the app bar.
- On mobile, web and console platforms, a
  `toga.MainWindow`{.interpreted-text role="class"} will include a title
  bar that can contain both menus and toolbar items.

Toolbar items can be added by adding them to
`~toga.MainWindow.toolbar`{.interpreted-text role="attr"}; any command
added to the toolbar will be automatically added to the App's commands
as well.

``` python
import toga

main_window = toga.MainWindow(title='My Application')

self.toga.App.main_window = main_window
main_window.show()
```

## Reference

::: {.autoclass}
toga.MainWindow
:::
