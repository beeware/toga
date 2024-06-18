from unittest.mock import Mock

import toga
from toga_dummy.utils import assert_action_not_performed, assert_action_performed


def test_create(app):
    """A MainWindow can be created with minimal arguments."""
    window = toga.MainWindow()

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create MainWindow")

    # This is a secondary main window; app menus have not been created, but
    # window menus and toolbars have been.
    assert_action_not_performed(window, "create App menus")
    assert_action_performed(window, "create Window menus")
    assert_action_performed(window, "create toolbar")

    # We can't know what the ID is, but it must be a string.
    assert isinstance(window.id, str)
    # Window title is the app title.
    assert window.title == "Test App"
    # The app has created a main window, so this will be the second window.
    assert window.position == (150, 150)
    assert window.size == (640, 480)
    assert window.resizable
    assert window.closable
    assert window.minimizable
    # No on-close handler
    assert window.on_close._raw is None

    # The window has an empty toolbar; but it's also a secondary MainWindow created
    # *after* the app has finished initializing; check it has a change handler
    assert len(window.toolbar) == 0
    assert window.toolbar.on_change is not None


def test_create_explicit(app):
    """Explicit arguments at construction are stored."""
    on_close_handler = Mock()
    window_content = toga.Box()

    window = toga.MainWindow(
        id="my-window",
        title="My Window",
        position=toga.Position(10, 20),
        size=toga.Position(200, 300),
        resizable=False,
        minimizable=False,
        content=window_content,
        on_close=on_close_handler,
    )

    assert window.app == app
    assert window.content == window_content

    window_content.window == window
    window_content.app == app

    assert window._impl.interface == window
    assert_action_performed(window, "create MainWindow")

    # This is a secondary main window; app menus have not been created, but
    # window menus and toolbars have been.
    assert_action_not_performed(window, "create App menus")
    assert_action_performed(window, "create Window menus")
    assert_action_performed(window, "create toolbar")

    assert window.id == "my-window"
    assert window.title == "My Window"
    assert window.position == toga.Position(10, 20)
    assert window.size == toga.Size(200, 300)
    assert not window.resizable
    assert window.closable
    assert not window.minimizable
    assert window.on_close._raw == on_close_handler

    # The window has an empty toolbar; but it's also a secondary MainWindow created
    # *after* the app has finished initializing; check it has a change handler
    assert len(window.toolbar) == 0
    assert window.toolbar.on_change is not None


def test_toolbar_implicit_add(app):
    """Adding an item to a toolbar implicitly adds it to the app."""
    # Use the toolbar on the app's main window
    window = app.main_window

    # Clear the app commands to start with
    app.commands.clear()
    assert list(window.toolbar) == []
    assert list(app.commands) == []

    cmd1 = toga.Command(None, "Command 1")
    cmd2 = toga.Command(None, "Command 2")

    assert list(window.toolbar) == []
    assert list(app.commands) == []

    # Adding a command to the toolbar automatically adds it to the app
    window.toolbar.add(cmd1)
    assert list(window.toolbar) == [cmd1]
    assert list(app.commands) == [cmd1]

    # But not vice versa
    app.commands.add(cmd2)
    assert list(window.toolbar) == [cmd1]
    assert list(app.commands) == [cmd1, cmd2]

    # Adding a command to both places does not cause a duplicate
    app.commands.add(cmd1)
    assert list(window.toolbar) == [cmd1]
    assert list(app.commands) == [cmd1, cmd2]
