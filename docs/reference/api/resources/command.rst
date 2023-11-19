Command
=======

A representation of app functionality that the user can invoke from menus or toolbars.

.. rst-class:: widget-support
.. csv-filter:: Availability (:ref:`Key <api-status-key>`)
   :header-rows: 1
   :file: ../../data/widgets_by_platform.csv
   :included_cols: 4,5,6,7,8,9,10
   :exclude: {0: '(?!(Command|Component))'}


Usage
-----

Aside from event handlers on widgets, most GUI toolkits also provide other ways for
the user to give instructions to an app. In Toga, these UI patterns are supported
by the :class:`~toga.Command` class.

A command encapsulates a piece of functionality that the user can invoke - no matter how
they invoke it. It doesn't matter if they select a menu item, press a button on a
toolbar, or use a key combination - the functionality is wrapped up in a Command.

Commands are added to an app using the properties :any:`toga.App.commands` and
:any:`toga.Window.toolbar`. Toga then takes control of ensuring that the
command is exposed to the user in a way that they can access. On desktop platforms,
this may result in a command being added to a menu.

Commands can be organized into a :class:`~toga.Group` of similar commands. Groups are
hierarchical, so a group can contain a sub-group, which can contain a sub-group, and so
on. Inside a group, commands can be organized into sections.

For example:

.. code-block:: python

    import toga

    def callback(sender, **kwargs):
        print("Command activated")

    stuff_group = Group('Stuff', order=40)

    cmd1 = toga.Command(
        callback,
        label='Example command',
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

This code defines a command ``cmd1`` that will be placed in the first section of the
"Stuff" group. It can be activated by pressing CTRL-k (or CMD-K on a Mac).

The definitions for ``cmd2``, ``cmd3``, and ``cmd4`` have been omitted, but would follow
a similar pattern.

It doesn't matter what order you add commands to the app - the group, section and order
will be used to display the commands in the right order.

If a command is added to a toolbar, it will automatically be added to the app as well.
It isn't possible to have functionality exposed on a toolbar that isn't also exposed by
the app. So, ``cmd2`` will be added to the app, even though it wasn't explicitly added
to the app commands.

Status Item Groups
~~~~~~~~~~~~~~~~~~

Top level groups (i.e., groups without a parent) can be declared as a *Status item*
group. Status item groups are *not* added to the main menu; instead, an icon will be
added to the system tray or notification bar, and the Commands associated with the group
will be displayed in a menu when the status icon is clicked.

If an app declares one or more status items, the first status item group (by numerical
ordering) will be interpreted as the main status item. This item will have default app
control commands (such as "About" and "Exit" commands) automatically added as the last
items in the group.

Notes
-----

* Status item groups are supported on GTK using the `Ayatana App Indicators
  <https://ayatanaindicators.github.io>`__ library. If this library (and it's GTK3
  PyGObject bindings) are not present, your app will raise an error at runtime.

  However, even if the Ayatana App Indicators library is present, *your app may not
  display status icons*. The GNOME team has a `philosophical objection to the concept of
  status icons <https://blogs.gnome.org/aday/2017/08/31/status-icons-and-gnome/>`__, and
  as a result, the default GNOME desktop experience does not support status indicator
  icons. They *can* be enabled through the use of `a GNOME shell extension
  <https://github.com/ubuntu/gnome-shell-extension-appindicator>`__, but this is not
  installed by default for most users. Toga has no way to detect if the user's
  environment supports status indicators, so there is not guarantee that any status
  indicators provided by your app will be visible. If your app is using a status item as
  the only user interface (e.g., in a :ref:`Windowless app
  </reference/api/windowlessapp>`__), this may result in an app that appears to do
  nothing, but raises no errors.

Reference
---------

.. autoclass:: toga.Command
    :exclude-members: key

.. autoclass:: toga.Group
    :exclude-members: key

.. autoprotocol:: toga.command.ActionHandler
