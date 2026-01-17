{{ component_header("Command") }}

## Usage

Aside from event handlers on widgets, most GUI toolkits also provide other ways for the user to give instructions to an app. In Toga, these UI patterns are supported by the [`Command`][toga.Command] class.

A command encapsulates a piece of functionality that the user can invoke - no matter how they invoke it. It doesn't matter if they select a menu item, press a button on a toolbar, or use a key combination - the functionality is wrapped up in a Command.

## Adding commands

Commands are added to an app using the properties [`toga.App.commands`][] and [`toga.MainWindow.toolbar`][]. Toga then takes control of ensuring that the command is exposed to the user in a way that they can access. On desktop platforms, this may result in a command being added to a menu.

Commands can be organized into a [`Group`][toga.Group] of similar commands. Groups are hierarchical, so a group can contain a sub-group, which can contain a sub-group, and so on. Inside a group, commands can be organized into sections.

For example:

```python
import toga

def callback(sender, **kwargs):
    print("Command activated")

stuff_group = toga.Group('Stuff', order=40)

cmd1 = toga.Command(
    callback,
    text='Example command',
    tooltip='Tells you when it has been activated',
    shortcut=toga.Key.MOD_1 + 'k',
    icon='icons/pretty.png',
    group=stuff_group,
    section=0
)
cmd2 = toga.Command(
    ...
)
...

app.commands.add(cmd1, cmd4, cmd3)
app.main_window.toolbar.add(cmd2, cmd3)
```

This code defines a command `cmd1` that will be placed in the first section of the "Stuff" group. It can be activated by pressing CTRL-k (or CMD-K on a Mac).

The definitions for `cmd2`, `cmd3`, and `cmd4` have been omitted, but would follow a similar pattern.

It doesn't matter what order you add commands to the app - the group, section and order will be used to display the commands in the right order.

If a command is added to a toolbar, it will automatically be added to the app as well. It isn't possible to have functionality exposed on a toolbar that isn't also exposed by the app. So, `cmd2` will be added to the app, even though it wasn't explicitly added to the app commands.

## Removing commands

Commands can be removed using set-like and dictionary-like APIs. The set-like APIs use the command instance; the dictionary-like APIs use the command ID:

```python
# Remove the app using the instance
app.commands.remove(cmd_1)

# Remove a command by ID
del app.commands["Some-Command-ID"]
```

## Standard commands

Each command has an [`id`][toga.Command.id] attribute. This is set when the command is defined; if no ID is provided, a random ID will be generated for the Command. This identifier can be used to retrieve a command from [`toga.App.commands`][] and [`toga.MainWindow.toolbar`][].

These command IDs are also used to create *standard* commands. These are commands that are expected functionality in most applications, such as [`ABOUT`][toga.Command.ABOUT] and [`EXIT`][toga.Command.EXIT], as well as document management commands such as [`NEW`][toga.Command.NEW], [`OPEN`][toga.Command.OPEN] and [`SAVE`][toga.Command.SAVE].

These commands are automatically added to your app, depending on platform requirements and app definition. For example, mobile apps won't have an Exit command as mobile apps don't have a concept of "exiting". Document management commands will be automatically added if your app defines [document types](../data-representation/document.md).

The label, shortcut, grouping and ordering of these commands is platform dependent. For example, on macOS, the [`EXIT`][toga.Command.EXIT] command will be labeled "Quit My App", and have a shortcut of Command-q; on Windows, the command will be labeled "Exit", and won't have a keyboard shortcut.

Any automatically added standard commands will be installed *before* your app's [`startup()`][toga.App.startup] method is invoked. If you wish to remove or modify and a standard app command, you can use the standard command's ID to retrieve the command instance from [`toga.App.commands`][]. If you wish to add or override a standard command that hasn't been installed by default (for example, to add an Open command without defining a document type), you can use the [toga.Command.standard()][toga.Command.standard] method to create an instance of the standard command, and add that command to your app:

```python
import toga

class MyApp(toga.app):
    def startup(self):
        ...
        # Delete the default Preferences command
        del self.commands[toga.Command.PREFERENCES]

        # Modify the text of the "About" command
        self.commands[toga.Command.ABOUT].text = "I'm Customized!!"

        # Add an Open command
        custom_open = toga.Command.standard(
            self,
            toga.Command.OPEN,
            action=self.custom_open
        )

        self.commands.add(custom_open)
```

## Reference

::: toga.Command

::: toga.Group

::: toga.command.CommandSet

::: toga.command.Separator

::: toga.command.ActionHandler

::: toga.command.CommandSetChangeHandler
