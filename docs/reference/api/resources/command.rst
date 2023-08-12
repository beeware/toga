Command
=======

A representation of app functionality that the user can invoke from menus or toolbars.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9
   :exclude: {0: '(?!(Command|Component))'}


Usage
-----

A GUI requires more than just widgets laid out in a user interface - you'll also want to
allow the user to actually *do* something. In Toga, you do this using
:class:`~toga.Command`.

A command encapsulates a piece of functionality that the user can invoke - no matter how
they invoke it. It doesn't matter if they select a menu item, press a button on a
toolbar, or use a key combination - the functionality is wrapped up in a Command.

When a command is added to an application, Toga takes control of ensuring that the
command is exposed to the user in a way that they can access it. On desktop platforms,
this may result in a command being added to a menu.

Commands can then be organized into a :class:`~toga.Group` of similar commands; inside a
group, commands can be organized into sections. Groups are also hierarchical, so a group
can contain a sub-group, which can contain a sub-group, and so on.

A collection of groups and commands is called a :class:`~toga.CommandSet`. The menus of
an app and the toolbar on a window are both examples of CommandSets.

Defining Commands
~~~~~~~~~~~~~~~~~

When you specify a :class:`~toga.Command`, you provide some additional metadata to help
classify and organize the commands in your application:

* **action**: A handler to invoke when the command is activated.

* **text**: A short label for the command.

* **tooltip**: A short description of what the command will do

* **shortcut**: (optional) A key combination that can be used to invoke the command.

* **icon**: (optional) A path to an icon resource to decorate the command.

* **group**: (optional) A :class:`~toga.Group` object describing a collection of similar commands.
  If no group is specified, a default "Command" group will be used.

* **section**: (optional) An integer providing a sub-grouping. If no section is
  specified, the command will be allocated to section 0 within the group.

* **order**: (optional) An integer indicating where a command falls within a section.
  If a :class:`~toga.Command` doesn't have an order, it will be sorted alphabetically by label
  within its section.

Commands may not use all the metadata - for example, on some platforms, menus
will contain icons; on other platforms they won't. Toga will use the metadata
if it is provided, but ignore it (or substitute an appropriate default) if it
isn't.

Commands can be enabled and disabled; if you disable a command, it will
automatically disable any toolbar or menu item where the command appears.

Defining Groups
~~~~~~~~~~~~~~~

When you specify a :class:`~toga.Group`, you provide some additional metadata to help
classify and organize the commands in your application:

* **text**: A short label for the group.

* **section**: (optional) An integer providing a sub-grouping. If no section is
  specified, the command will be allocated to section 0 within the group.

* **order**: (optional) An integer indicating where a command falls within a section.
  If a :class:`~toga.Command` doesn't have an order, it will be sorted alphabetically by label
  within its section.

* **parent**: (optional) The parent :class:`~toga.Group` of this group (if any).

Toga provides a number of ready-to-use groups:

* ``Group.APP`` - Application level control
* ``Group.FILE`` - File commands
* ``Group.EDIT`` - Editing commands
* ``Group.VIEW`` - Commands to alter the appearance of content
* ``Group.COMMANDS`` - A default group for user-provided commands
* ``Group.WINDOW`` - Commands for managing windows in the app
* ``Group.HELP`` - Help content

Example
~~~~~~~

The following is an example of using menus and commands:

.. code-block:: python

    import toga

    def callback(sender, **kwargs):
        print("Command activated")

    stuff_group = Group('Stuff', order=40)

    cmd1 = toga.Command(
        callback,
        label='Example command',
        tooltip='Tells you when it has been activated',
        shortcut='k',
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

This code defines a command ``cmd1`` that will be placed in the first section of the
"Stuff" group. It can be activated by pressing CTRL-k (or CMD-K on a Mac).

The definitions for ``cmd2``, ``cmd3``, and ``cmd4`` have been omitted, but would follow
a similar pattern.

It doesn't matter what order you add commands to the app - the group, section and order
will be used to put the commands in the right order.

If a command is added to a toolbar, it will automatically be added to the app
as well. It isn't possible to have functionality exposed on a toolbar that
isn't also exposed by the app. So, ``cmd2`` will be added to the app, even though
it wasn't explicitly added to the app commands.

Reference
---------

.. autoprotocol:: toga.command.ActionHandler

.. autoclass:: toga.Command
   :members:
   :undoc-members:

.. autoclass:: toga.Group
   :members:
   :undoc-members:

.. autoprotocol:: toga.command.CommandSetChangeHandler

.. autoclass:: toga.command.CommandSet
   :members:
   :undoc-members:
