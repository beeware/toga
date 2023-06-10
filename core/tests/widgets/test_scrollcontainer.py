from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def app():
    return toga.App("Scroll Container Test", "org.beeware.toga.scroll_container")


@pytest.fixture
def window():
    return toga.Window()


@pytest.fixture
def content():
    return toga.Box()


@pytest.fixture
def on_scroll_handler():
    return Mock()


@pytest.fixture
def scroll_container(content, on_scroll_handler):
    return toga.ScrollContainer(content=content, on_scroll=on_scroll_handler)


def test_widget_created():
    "A scroll container can be created with no arguments"
    scroll_container = toga.ScrollContainer()
    assert scroll_container._impl.interface == scroll_container
    assert_action_performed(scroll_container, "create ScrollContainer")

    assert scroll_container.content is None
    assert scroll_container.vertical
    assert scroll_container.horizontal
    assert scroll_container.on_scroll._raw is None


def test_widget_created_with_values(content, on_scroll_handler):
    "A scroll container can be created with arguments"
    scroll_container = toga.ScrollContainer(
        content=content,
        on_scroll=on_scroll_handler,
        vertical=False,
        horizontal=False,
    )
    assert scroll_container._impl.interface == scroll_container
    assert_action_performed(scroll_container, "create ScrollContainer")

    assert scroll_container.content == content
    assert not scroll_container.vertical
    assert not scroll_container.horizontal
    assert scroll_container.on_scroll._raw == on_scroll_handler

    # The content has been assigned to the widget
    assert_action_performed_with(scroll_container, "set content", widget=content)

    # The scroll container has been refreshed
    assert_action_performed(scroll_container, "refresh")

    # The content and the frame has been refreshed
    assert_action_performed(content, "refresh")

    # The scroll handler hasn't been invoked
    on_scroll_handler.assert_not_called()


def test_assign_to_app(app, scroll_container, content):
    """If the widget is assigned to an app, the content is also assigned"""
    # Scroll container is initially unassigned
    assert scroll_container.app is None

    # Assign the scroll container to the app
    scroll_container.app = app

    # Scroll container is on the app
    assert scroll_container.app == app
    # Content is also on the app
    assert content.app == app


def test_assign_to_app_no_content(app):
    """If the widget is assigned to an app, and there is no content, there's no error"""
    scroll_container = toga.ScrollContainer()

    # Scroll container is initially unassigned
    assert scroll_container.app is None

    # Assign the scroll container to the app
    scroll_container.app = app

    # Scroll container is on the app
    assert scroll_container.app == app


def test_assign_to_window(window, scroll_container, content):
    """If the widget is assigned to a window, the content is also assigned"""
    # Scroll container is initially unassigned
    assert scroll_container.window is None

    # Assign the scroll container to the window
    scroll_container.window = window

    # Scroll container is on the window
    assert scroll_container.window == window
    # Content is also on the window
    assert content.window == window


def test_assign_to_window_no_content(window):
    """If the widget is assigned to an app, and there is no content, there's no error"""
    scroll_container = toga.ScrollContainer()

    # Scroll container is initially unassigned
    assert scroll_container.window is None

    # Assign the scroll container to the window
    scroll_container.window = window

    # Scroll container is on the window
    assert scroll_container.window == window


def test_disable_no_op(scroll_container):
    "ScrollContainer doesn't have a disabled state"
    # Enabled by default
    assert scroll_container.enabled

    # Try to disable the widget
    scroll_container.enabled = False

    # Still enabled.
    assert scroll_container.enabled


def test_focus_noop(scroll_container):
    "Focus is a no-op."

    scroll_container.focus()
    assert_action_not_performed(scroll_container, "focus")


def test_set_content(app, window, scroll_container, content):
    """The content of the scroll container can be changed"""
    # Assign the scroll container to an app and window
    scroll_container.app = app
    scroll_container.window = window

    # The content is also assigned
    assert content.app == app
    assert content.window == window

    # Reset the event log
    EventLog.reset()

    # Create new content, and assign it to the scroll container
    new_content = toga.Box()
    scroll_container.content = new_content

    # The content has been assigned to the widget
    assert_action_performed_with(scroll_container, "set content", widget=new_content)

    # The scroll container has been refreshed
    assert_action_performed(scroll_container, "refresh")

    # The new content has been refreshed
    assert_action_performed(new_content, "refresh")

    # The content has been assigned
    assert scroll_container.content == new_content

    # The new content is assigned to
    assert new_content.app == app
    assert new_content.window == window

    # The old content isn't
    assert content.app is None
    assert content.window is None


def test_clear_content(app, window, scroll_container, content):
    """The content of the scroll container can be cleared"""
    # Assign the scroll container to an app and window
    scroll_container.app = app
    scroll_container.window = window

    # The content is also assigned
    assert content.app == app
    assert content.window == window

    # Reset the event log
    EventLog.reset()

    # Clear the content
    scroll_container.content = None

    # The content has been assigned to the widget
    assert_action_performed_with(scroll_container, "set content", widget=None)

    # The scroll container has been refreshed
    assert_action_performed(scroll_container, "refresh")

    # The content has been cleared
    assert scroll_container.content is None

    # The old content isn't assigned any more
    assert content.app is None
    assert content.window is None


@pytest.mark.parametrize(
    "value, expected",
    [
        (True, True),
        (False, False),
        (42, True),
        (0, False),
        ("True", True),
        ("False", True),  # non-empty string is truthy
        ("", False),
        (object(), True),
    ],
)
def test_horizontal(scroll_container, content, value, expected):
    "Horizontal scrolling can be enabled/disabled."
    scroll_container.horizontal = value
    scroll_container.horizontal == expected

    # Content is refreshed as a result of the change
    assert_action_performed(content, "refresh")


@pytest.mark.parametrize(
    "value, expected",
    [
        (True, True),
        (False, False),
        (42, True),
        (0, False),
        ("True", True),
        ("False", True),  # non-empty string is truthy
        ("", False),
        (object(), True),
    ],
)
def test_vertical(scroll_container, content, value, expected):
    "Vertical scrolling can be enabled/disabled."
    scroll_container.vertical = value
    scroll_container.vertical == expected

    # Content is refreshed as a result of the change
    assert_action_performed(content, "refresh")


def test_horizontal_position(scroll_container):
    "The horizontal position can be set and retrieved"
    scroll_container.horizontal_position = 10

    assert scroll_container.horizontal_position == 10
    assert scroll_container.max_horizontal_position == 1000


def test_get_horizontal_position_when_not_horizontal(scroll_container):
    "If horizontal scrolling isn't enabled, getting the horizontal position raises an error"
    scroll_container.horizontal = False

    assert scroll_container.horizontal_position is None
    assert scroll_container.max_horizontal_position is None


def test_horizontal_position_when_not_horizontal(scroll_container):
    "If horizontal scrolling isn't enabled, setting the horizontal position raises an error"
    scroll_container.horizontal = False
    with pytest.raises(
        ValueError,
        match=r"Cannot set horizontal position when horizontal is not set.",
    ):
        scroll_container.horizontal_position = 0.5


def test_vertical_position(scroll_container):
    "The vertical position can be set and retrieved"
    scroll_container.vertical_position = 10

    assert scroll_container.vertical_position == 10
    assert scroll_container.max_vertical_position == 2000


def test_get_vertical_position_when_not_vertical(scroll_container):
    "If vertical scrolling isn't enabled, getting the vertical position raises an error"
    scroll_container.vertical = False

    assert scroll_container.vertical_position is None
    assert scroll_container.max_vertical_position is None


def test_set_vertical_position_when_not_vertical(scroll_container):
    "If vertical scrolling isn't enabled, setting the vertical position raises an error"
    scroll_container.vertical = False
    with pytest.raises(
        ValueError,
        match=r"Cannot set vertical position when vertical is not set.",
    ):
        scroll_container.vertical_position = 0.5
