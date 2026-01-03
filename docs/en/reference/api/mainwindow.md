{{ component_header("MainWindow", width=450) }}

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

## Notes

- On iOS:
  - Icons for toolbars should be alpha masks.
  - Toga does not currently provide mechanisms to access system icons, which iOS recommends, so icons should be iOS-compatible and used consistently within all scenes of your app.
  - On iOS 26+, icons in different sections will have their "liquid glass" panes separated; a short distance will be inserted in previous versions.
  - On iOS 26+, icons may also be moved to an overflow menu if there is not enough space to fit.  It is best to avoid overflowing menus, which do not exist automatically on older systems.
  - Icons are preferred to text in toolbar menus; an icon will be shown if it is provided, else the text.  Icon and text will always have separated glass sections on iOS 26+.
  - The iOS Human Interface Guidelines differentiate between normal and prominent actions.  Any command with a text of Done, Save, or Submit will be automatically promoted to a prominent action, which has a separate glass pane on iOS 26+.


## Reference

::: toga.MainWindow
