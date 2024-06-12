from unittest.mock import Mock

import toga
from toga_dummy.utils import assert_action_performed


def test_create(app):
    """A MainWindow can be created with minimal arguments."""
    window = toga.MainWindow()

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create MainWindow")

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
    assert len(window.toolbar) == 0
    # No on-close handler
    assert window.on_close._raw is None


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

    assert window.id == "my-window"
    assert window.title == "My Window"
    assert window.position == toga.Position(10, 20)
    assert window.size == toga.Size(200, 300)
    assert not window.resizable
    assert window.closable
    assert not window.minimizable
    assert len(window.toolbar) == 0
    assert window.on_close._raw == on_close_handler
