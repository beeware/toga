from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import assert_action_performed


def test_create(app):
    "A MainWindow can be created with minimal arguments"
    window = toga.MainWindow()

    assert window.app == app
    assert window.content is None

    assert window._impl.interface == window
    assert_action_performed(window, "create Window")

    # We can't know what the ID is, but it must be a string.
    assert isinstance(window.id, str)
    # Window title is the app title.
    assert window.title == "Test App"
    assert window.position == (100, 100)
    assert window.size == (640, 480)
    assert window.resizable
    assert window.closable
    assert window.minimizable
    assert len(window.toolbar) == 0
    # No on-close handler
    assert window.on_close is None


def test_no_close():
    "An on_close handler cannot be set on MainWindow"
    window = toga.MainWindow()

    with pytest.raises(
        ValueError,
        match=r"Cannot set on_close handler for the main window. Use the app on_exit handler instead.",
    ):
        window.on_close = Mock()
