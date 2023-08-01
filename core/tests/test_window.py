from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def app():
    return toga.App("Test App", "org.beeware.toga.window")


@pytest.fixture
def window():
    return toga.Window()


def test_window_created():
    "A Window can be created with minimal arguments"
    window = toga.Window()

    assert window.app is None
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create Window")

    # We can't know what the ID is, but it must be a string.
    assert isinstance(window.id, str)
    assert window.title == "Toga"
    assert window.position == (100, 100)
    assert window.size == (640, 480)
    assert window.resizeable
    assert window.closeable
    assert window.minimizable
    assert len(window.toolbar) == 0
    assert window.on_close._raw is None


def test_window_created_explicit():
    "Explicit arguments at construction are stored"
    on_close_handler = Mock()

    window = toga.Window(
        id="my-window",
        title="My Window",
        position=(10, 20),
        size=(200, 300),
        resizeable=False,
        closeable=False,
        minimizable=False,
        on_close=on_close_handler,
    )

    assert window.app is None
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create Window")

    assert window.id == "my-window"
    assert window.title == "My Window"
    assert window.position == (10, 20)
    assert window.size == (200, 300)
    assert not window.resizeable
    assert not window.closeable
    assert not window.minimizable
    assert len(window.toolbar) == 0
    assert window.on_close._raw == on_close_handler


def test_set_app(window, app):
    """A window can be assigned to an app"""
    assert window.app is None

    window.app = app

    assert window.app == app

    app2 = toga.App("Test App 2", "org.beeware.toga.window2")
    with pytest.raises(ValueError, match=r"Window is already associated with an App"):
        window.app = app2


def test_set_app_with_content(window, app):
    """If a window has content, the content is assigned to the app"""
    content = toga.Box()
    window.content = content

    assert window.app is None
    assert content.app is None

    window.app = app

    assert window.app == app
    assert content.app == app


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", "Toga"),
        (None, "Toga"),
        (12345, "12345"),
        ("Contains\nnewline", "Contains"),
    ],
)
def test_title(window, value, expected):
    """The title of the window can be changed"""
    window.title = value
    assert window.title == expected


def test_change_content(window, app):
    """The content of a window can be changed"""
    window.app = app
    assert window.content is None
    assert window.app == app

    # Set the content of the window
    content1 = toga.Box()
    window.content = content1

    # The content has been assigned and refreshed
    assert content1.app == app
    assert content1.window == window
    assert_action_performed_with(window, "set content", widget=content1._impl)
    assert_action_performed(content1, "refresh")

    # Set the content of the window to something new
    content2 = toga.Box()
    window.content = content2

    # The content has been assigned and refreshed
    assert content2.app == app
    assert content2.window == window
    assert_action_performed_with(window, "set content", widget=content2._impl)
    assert_action_performed(content2, "refresh")

    # The original content has been removed
    assert content1.window is None


def test_set_position(window):
    """The position of the window can be set."""
    window.position = (123, 456)

    assert window.position == (123, 456)


def test_set_size(window):
    """The size of the window can be set."""
    window.size = (123, 456)

    assert window.size == (123, 456)


def test_set_size_with_content(window):
    """The size of the window can be set."""
    content = toga.Box()
    window.content = content

    window.size = (123, 456)

    assert window.size == (123, 456)
    assert_action_performed(content, "refresh")


def test_show_hide(window, app):
    """The window can be shown and hidden."""
    assert window.app is None

    window.show()

    # The window has been assigned to the app, and is visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "show")
    assert window.visible

    # Hide with an explicit call
    window.hide()

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "hide")
    assert not window.visible


def test_hide_show(window, app):
    """The window can be hidden then shown."""
    assert window.app is None

    window.hide()

    # The window has been assigned to the app, and is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "hide")
    assert not window.visible

    # Show with an explicit call
    window.show()

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "show")
    assert window.visible


def test_visibility(window, app):
    """The window can be shown and hidden using the visible property."""
    assert window.app is None

    window.visible = True

    # The window has been assigned to the app, and is visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "show")
    assert window.visible

    # Hide with an explicit call
    window.visible = False

    # Window is still assigned to the app, but is not visible
    assert window.app == app
    assert window in app.windows
    assert_action_performed(window, "hide")
    assert not window.visible


def test_close_no_handler(window, app):
    """A window without a close handler can be closed"""
    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")


def test_close_sucessful_handler(window, app):
    """A window with a successful close handler can be closed"""
    on_close_handler = Mock(return_value=True)
    window.on_close = on_close_handler

    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.app == app
    assert window not in app.windows
    assert_action_performed(window, "close")
    on_close_handler.assert_called_once_with(window)


def test_close_rejected_handler(window, app):
    """A window can have a close handler that rejects closing"""
    on_close_handler = Mock(return_value=False)
    window.on_close = on_close_handler

    window.show()
    assert window.app == app
    assert window in app.windows

    # Close the window
    window._impl.simulate_close()

    # Window has been closed, and is no longer in the app's list of windows.
    assert window.app == app
    assert window in app.windows
    assert_action_not_performed(window, "close")
    on_close_handler.assert_called_once_with(window)
