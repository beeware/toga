{{ component_header("Status icons", width=150) }}

## Usage

Although the usual user interface for an app is a window, some apps will augment - or even replace - a window-base interface with an icon in the system tray or status bar provided by the operating system. This is especially common for apps that primarily run in the background.

Toga supports two types of status icons - simple status icons, and menu status icons.

### Simple status icons

A simple status icon is a bare icon in the status bar. You can set and change the icon as required to reflect changes in application state; by default, the status icon will use the app's icon. The text associated with the icon will be used as a tooltip; again, the app's formal name will be used as default text. The icon can respond to mouse clicks by defining an `on_press` handler.

To define a simple status icon, declare an instance of [`toga.SimpleStatusIcon`][], and add it to your app's [`status_icons`][toga.App.status_icons] set:

```python
import toga

# Define a status icon that uses default values for icon and tooltip,
# and doesn't respond to mouse clicks.
status_icon_1 = toga.SimpleStatusIcon()

# Define a second status icon that provides explicit values for the id, icon and
# tooltip, and responds to mouse clicks.
def my_handler(widget, **kwargs):
    print("Second status icon pressed!")

status_icon_2 = toga.SimpleStatusIcon(
    id="second",
    text="Hello!",
    icon="icons/red",
    on_press=my_handler
)

# Add both status icons to the app
app.status_icons.add(status_icon_1, status_icon_2)
```

Once a status icon has been added to the app, it can be retrieved by ID or by index; and it can be removed from the app:

```python
# Change the icon of the first status icon, retrieved by index:
app.status_icons[0].icon = "icons/green"

# Change the icon of the second status icon, retrieved by id:
app.status_icons["second"].icon = "icons/blue"

# Remove the first status icon from the app:
app.status_icons.remove(status_icon_1)
```

### Menu status icons

A menu-based status icon is defined by adding a [`toga.MenuStatusIcon`][] instance. A [`toga.MenuStatusIcon`][] behaves almost the same as [`SimpleStatusIcon`][toga.SimpleStatusIcon], except that it *cannot* have an `on_click` handler - but it *can* be used to register Commands that will be displayed in a menu when the icon is clicked.

The [`MenuStatusIcon`][toga.MenuStatusIcon] is a [`Group`][toga.Group] for command sorting purposes. To put a command in a menu associated with a [`MenuStatusIcon`][toga.MenuStatusIcon], set the `group` associated with that command, then add the command to the [`CommandSet`][toga.command.CommandSet] associated with status icons. The following example will create a [`MenuStatusIcon`][toga.MenuStatusIcon] that has a single top-level menu item, plus a sub-menu that itself has a single menu item:

```python
# Create a MenuStatusIcon
status_icon = toga.MenuStatusIcon(icon="icons/blue")

# Create some commands that are associated with the menu status icon's group.
def callback(sender, **kwargs):
    print("Command activated")

cmd1 = toga.Command(
    callback,
    text='Example command',
    group=status_icon,
)

# Create a sub-group of the status icon. This will appear as a submenu.
stuff_group = toga.Group('Stuff', parent=status_icon)

cmd2 = toga.Command(
    callback,
    text='Stuff sub-command',
    group=stuff_group
)

# Add the status icon to the app
app.status_icons.add(status_icon)

# Add the commands to the status icons command set
app.status_icons.commands.add(cmd1, cmd2)
```

If you add at least one [`MenuStatusIcon`][toga.MenuStatusIcon] instance to your app, Toga will add some standard commands to the app's status icon command set. These items will appear at the end of the first [`MenuStatusIcon`][toga.MenuStatusIcon]'s menu. To remove these items, clear the app's status icon command set before adding your own commands.

If you add a command to the app's status icon command set that *doesn't* belong to a [`MenuStatusIcon`][toga.MenuStatusIcon] group, or that belongs to a [`MenuStatusIcon`][toga.MenuStatusIcon] group that hasn't been registered with the app as a status icon, a `ValueError` will be raised. An error will also be raised if you *remove* a status icon while there status icon commands referencing that command.

## Notes

- Status icons on GTK are implemented using the [XApp](https://github.com/linuxmint/xapp) library. This requires that the user has installed the system packages for `libxapp`, plus the GObject Introspection bindings for that library. The name of the system package required is distribution dependent:
    - Ubuntu: `gir1.2-xapp-1.0`
    - Fedora: `xapps`
- The GNOME desktop environment does not provide built-in support for status icons. [This is an explicit design decision on their part](https://blogs.gnome.org/aday/2017/08/31/status-icons-and-gnome/), and they advise against using status icons as part of your app design. However, there are GNOME shell extensions that can add support for status icons. Other GTK-based desktop environments (such as Cinnamon) *do* support status icons.

## Reference

::: toga.statusicons.StatusIcon

::: toga.SimpleStatusIcon

::: toga.MenuStatusIcon

::: toga.statusicons.StatusIconSet
