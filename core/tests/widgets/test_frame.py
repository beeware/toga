import pytest

import toga
from toga_dummy.utils import (
    assert_action_performed,
    assert_action_performed_with,
    attribute_value,
)


@pytest.fixture
def window(app):
    return toga.Window()


@pytest.fixture
def content():
    return toga.Box()


@pytest.fixture
def frame(content):
    return toga.Frame(content=content)


def test_create():
    """A Frame can be created with no content or title."""
    frame = toga.Frame()
    assert frame._impl.interface == frame
    assert_action_performed(frame, "create Frame")

    assert frame.content is None
    assert frame.title == ""


def test_create_with_values():
    """A Frame can be created with content and a title."""
    content = toga.Box()
    frame = toga.Frame(content=content, title="Settings")

    assert frame._impl.interface == frame
    assert frame.content == content
    assert frame.title == "Settings"

    # Content is handed to the impl as the child's impl, and is refreshed.
    assert_action_performed_with(frame, "set content", widget=content._impl)
    assert_action_performed(content, "refresh")


def test_set_content(app, window):
    """Content can be (re)assigned, and inherits the frame's app and window."""
    window.content = toga.Box(children=[frame := toga.Frame()])

    new_content = toga.Box()
    frame.content = new_content

    assert_action_performed_with(frame, "set content", widget=new_content._impl)
    assert frame.content == new_content
    assert new_content.app == app
    assert new_content.window == window

    # Clearing the content removes it from the frame.
    frame.content = None
    assert frame.content is None
    assert_action_performed_with(frame, "set content", widget=None)


def test_assign_to_app(app, frame, content):
    """If the frame is assigned to an app, its content is assigned too."""
    # Frame is initially unassigned.
    assert frame.app is None

    # Assign the frame to the app.
    frame.app = app

    # Both the frame and its content are now on the app.
    assert frame.app == app
    assert content.app == app


def test_assign_to_app_no_content(app):
    """Assigning a content-less frame to an app doesn't error."""
    frame = toga.Frame()
    assert frame.app is None

    frame.app = app

    assert frame.app == app


def test_assign_to_window(window, frame, content):
    """If the frame is assigned to a window, its content is assigned too."""
    # Frame is initially unassigned.
    assert frame.window is None

    # Assign the frame to the window.
    frame.window = window

    # Both the frame and its content are now on the window.
    assert frame.window == window
    assert content.window == window


def test_assign_to_window_no_content(window):
    """Assigning a content-less frame to a window doesn't error."""
    frame = toga.Frame()
    assert frame.window is None

    frame.window = window

    assert frame.window == window


def test_title():
    """The title round-trips through the impl, coercing None to an empty string."""
    frame = toga.Frame()
    frame.title = "Alarms"
    assert frame.title == "Alarms"
    assert attribute_value(frame, "title") == "Alarms"

    frame.title = None
    assert frame.title == ""


def test_disable_no_op():
    """A Frame is always enabled; attempts to disable it are ignored."""
    frame = toga.Frame()
    assert frame.enabled

    frame.enabled = False
    assert frame.enabled


def test_focus_no_op():
    """A Frame cannot accept focus."""
    frame = toga.Frame()
    frame.focus()
