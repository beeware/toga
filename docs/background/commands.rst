============================
Commands, Menus and Toolbars
============================

A GUI requires more than just widgets laid out in a user interface - you'll
also want to allow the user to actually *do* something. In Toga, you do this
using ``Commands``.

A command encapsulates a piece of functionality that the user can invoke - no
matter how they invoke it. It doesn't matter if they select a menu item,
press a button on a toolbar, or use a key combination - the functionality is
wrapped up in a Command.

When a command is added to an application, Toga takes control of ensuring that
the command is exposed to the user in a way that they can access it. On desktop
platforms, this may result in a command being added to a menu.

You can also choose to add a command (or commands) to a toolbar on a specific
window.

Defining Commands
~~~~~~~~~~~~~~~~~

When you specify a ``Command``, you provide some additional metadata to help
classify and organize the commands in your application:

* An **action** - a function to invoke when the command is activated.

* A **label** - a name for the command to.

* A **tooltip** - a short description of what the command will do

* A **shortcut** - (optional) A key combination that can be used to invoke the command.

* An **icon** - (optional) A path to an icon resource to decorate the command.

* A **group** - (optional) a ``Group`` object describing a collection of similar commands. If no group is specified, a default "Command" group will be used.

* A **section** - (optional) an integer providing a sub-grouping. If no section is specified, the command will be allocated to section 0 within the group.

* An **order** - (optional) an integer indicating where a command falls within a section. If a ``Command`` doesn't have an order, it will be sorted alphabetically by label within it's section.

Commands may not use all the metadata - for example, on some platforms, menus
will contain icons; on other platforms, they won't. Toga will use the metadata
if it is provided, but ignore it (or substitute an appropriate default) if it
isn't.

Commands can be enabled and disabled; if you disable a command, it will
automatically disable any toolbar or menu item where the command appears.

Groups
~~~~~~

Toga provides a number of ready-to-use groups:

* ``Group.APP`` - Application level control
* ``Group.FILE`` - File commands
* ``Group.EDIT`` - Editing commands
* ``Group.VIEW`` - Commands to alter the appearance of content
* ``Group.COMMANDS`` - A Default
* ``Group.WINDOW`` - Commands for managing different windows in the app
* ``Group.HELP`` - Help content

You can also define custom groups.

Example
~~~~~~~

The following is an example of using menus and commands::

    import toga

    def callback(sender):
        print("Command activated")

    def build(app):
        ...
        stuff_group = Group('Stuff', order=40)

        cmd1 = toga.Command(
            callback,
            label='Example command',
            tooltip='Tells you when it has been activated',
            shortcut='k',
            icon='icons/pretty.png'
            group=stuff_group,
            section=0
        )
        cmd2 = toga.Command(
            ...
        )
        ...

        app.commands.add(cmd1, cmd4, cmd3)
        app.main_window.toolbar.add(cmd2, cmd3)

This code defines a command ``cmd1`` that will be placed in first section of
the "Stuff" group. It can be activated by pressing CTRL-k (or CMD-K on a Mac).

The definitions for ``cmd2``, ``cmd3``, and ``cmd4`` have been omitted, but would
follow a similar pattern.

It doesn't matter what order you add commands to the app - the group, section
and order will be used to put the commands in the right order.

If a command is added to a toolbar, it will automatically be added to the app
as well. It isn't possible to have functionality exposed on a toolbar that
isn't also exposed by the app. So, ``cmd2`` will be added to the app, even though
it wasn't explicitly added to the app commands.
