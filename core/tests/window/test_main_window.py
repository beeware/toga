from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import (
    assert_action_performed,
)


@pytest.fixture
def window(app):
    return toga.MainWindow()


def test_window_created(app):
    "A Window can be created with minimal arguments"
    window = toga.MainWindow()

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create MainWindow")

    # We can't know what the ID is, but it must be a string.
    assert isinstance(window.id, str)
    assert window.title == "Test App"
    assert window.position == (100, 100)
    assert window.size == (640, 480)
    assert window.resizable
    assert window.closable
    assert window.minimizable
    assert window.on_close._raw is None


def test_window_created_explicit(app):
    "Explicit arguments at construction are stored"
    on_close_handler = Mock()

    window = toga.MainWindow(
        id="my-window",
        title="My Window",
        position=(10, 20),
        size=(200, 300),
        resizable=False,
        closable=False,
        minimizable=False,
        on_close=on_close_handler,
    )

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create MainWindow")

    assert window.id == "my-window"
    assert window.title == "My Window"
    assert window.position == (10, 20)
    assert window.size == (200, 300)
    assert not window.resizable
    assert not window.closable
    assert not window.minimizable
    assert window.on_close._raw == on_close_handler


def test_toolbar_implicit_add(window, app):
    """Adding an item to to a toolbar implicitly adds it to the app."""
    cmd1 = toga.Command(None, "Command 1")
    cmd2 = toga.Command(None, "Command 2")
    # The app has 3 commands that will come before user commands, and one after

    toolbar = window.toolbar
    assert list(toolbar) == []
    assert list(app.commands)[3:-1] == []

    # Adding a command to the toolbar automatically adds it to the app
    toolbar.add(cmd1)
    assert list(toolbar) == [cmd1]
    assert list(app.commands)[3:-1] == [cmd1]

    # But not vice versa
    app.commands.add(cmd2)
    assert list(toolbar) == [cmd1]
    assert list(app.commands)[3:-1] == [cmd1, cmd2]

    # Adding a command to both places does not cause a duplicate
    app.commands.add(cmd1)
    assert list(toolbar) == [cmd1]
    assert list(app.commands)[3:-1] == [cmd1, cmd2]
