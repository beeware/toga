import pytest

import toga
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def app():
    return toga.App("Split Container Test", "org.beeware.toga.split_container")


@pytest.fixture
def window():
    return toga.Window()


@pytest.fixture
def content1():
    return toga.Box()


@pytest.fixture
def content2():
    return toga.Box()


@pytest.fixture
def content3():
    return toga.Box()


@pytest.fixture
def splitcontainer(content1, content2):
    return toga.SplitContainer(content=[content1, content2])


def test_widget_created():
    "A scroll container can be created with no arguments"
    splitcontainer = toga.SplitContainer()
    assert splitcontainer._impl.interface == splitcontainer
    assert_action_performed(splitcontainer, "create SplitContainer")

    assert splitcontainer.content == []
    assert splitcontainer.direction == toga.SplitContainer.VERTICAL


def test_widget_created_with_values(content1, content2, content3):
    "A scroll container can be created with arguments"
    splitcontainer = toga.SplitContainer(
        content=[content1, content2, content3],
        direction=toga.SplitContainer.HORIZONTAL,
    )
    assert splitcontainer._impl.interface == splitcontainer
    assert_action_performed(splitcontainer, "create SplitContainer")

    assert splitcontainer.content == [content1, content2, content3]
    assert splitcontainer.direction == toga.SplitContainer.HORIZONTAL

    # The content has been assigned to the widget
    assert_action_performed_with(
        splitcontainer,
        "set content",
        content=[content1, content2, content3],
        flex=[1, 1, 1],
    )

    # The scroll container has been refreshed
    assert_action_performed(splitcontainer, "refresh")


def test_assign_to_app(app, splitcontainer, content1, content2):
    """If the widget is assigned to an app, the content is also assigned"""
    # Scroll container is initially unassigned
    assert splitcontainer.app is None

    # Assign the scroll container to the app
    splitcontainer.app = app

    # Scroll container is on the app
    assert splitcontainer.app == app

    # Content is also on the app
    assert content1.app == app
    assert content2.app == app


def test_assign_to_app_no_content(app):
    """If the widget is assigned to an app, and there is no content, there's no error"""
    splitcontainer = toga.SplitContainer()

    # Scroll container is initially unassigned
    assert splitcontainer.app is None

    # Assign the scroll container to the app
    splitcontainer.app = app

    # Scroll container is on the app
    assert splitcontainer.app == app


def test_assign_to_window(window, splitcontainer, content1, content2):
    """If the widget is assigned to a window, the content is also assigned"""
    # Scroll container is initially unassigned
    assert splitcontainer.window is None

    # Assign the scroll container to the window
    splitcontainer.window = window

    # Scroll container is on the window
    assert splitcontainer.window == window
    # Content is also on the window
    assert content1.window == window
    assert content2.window == window


def test_assign_to_window_no_content(window):
    """If the widget is assigned to an app, and there is no content, there's no error"""
    splitcontainer = toga.SplitContainer()

    # Scroll container is initially unassigned
    assert splitcontainer.window is None

    # Assign the scroll container to the window
    splitcontainer.window = window

    # Scroll container is on the window
    assert splitcontainer.window == window


def test_disable_no_op(splitcontainer):
    "SplitContainer doesn't have a disabled state"
    # Enabled by default
    assert splitcontainer.enabled

    # Try to disable the widget
    splitcontainer.enabled = False

    # Still enabled.
    assert splitcontainer.enabled


def test_focus_noop(splitcontainer):
    "Focus is a no-op."

    splitcontainer.focus()
    assert_action_not_performed(splitcontainer, "focus")


def test_set_content_widgets(
    splitcontainer,
    content1,
    content2,
    content3,
):
    """Widget content can be set to a list of widgets"""
    splitcontainer.content = [content1, content2, content3]

    assert_action_performed_with(
        splitcontainer,
        "set content",
        content=[content1, content2, content3],
        flex=[1, 1, 1],
    )

    # The scroll container has been refreshed
    assert_action_performed(splitcontainer, "refresh")


def test_set_content_flex(splitcontainer, content1, content2, content3):
    """Widget content can be set to a list of widgets with flex values"""
    splitcontainer.content = [(content1, 1), (content2, 2), (content3, 3)]

    assert_action_performed_with(
        splitcontainer,
        "set content",
        content=[content1, content2, content3],
        flex=[1, 2, 3],
    )

    # The scroll container has been refreshed
    assert_action_performed(splitcontainer, "refresh")


def test_set_content_flex_altered(splitcontainer, content1, content2):
    """Flex values will be manipulated if out of range, and defaulted if missing"""
    splitcontainer.content = [content1, (content2, 0)]

    assert_action_performed_with(
        splitcontainer,
        "set content",
        content=[content1, content2],
        flex=[1, 1],
    )

    # The scroll container has been refreshed
    assert_action_performed(splitcontainer, "refresh")


@pytest.mark.parametrize(
    "content, message",
    [
        (
            None,
            r"SplitContainer content must be a list of at least 2 elements",
        ),
        (
            [],
            r"SplitContainer content must be a list of at least 2 elements",
        ),
        (
            [toga.Box()],
            r"SplitContainer content must be a list of at least 2 elements",
        ),
        (
            [toga.Box(), (toga.Box(),)],
            r"An item in SplitContainer content must be a 2-tuple containing "
            r"the widget, and the flex weight to assign to that widget.",
        ),
        (
            [toga.Box(), (toga.Box(), 42, True)],
            r"An item in SplitContainer content must be a 2-tuple containing "
            r"the widget, and the flex weight to assign to that widget.",
        ),
    ],
)
def test_set_content_invalid(splitcontainer, content, message):
    """Widget content can only be set to valid values"""

    with pytest.raises(ValueError, match=message):
        splitcontainer.content = content


def test_direction(splitcontainer):
    """The direction of the splitcontainer can be changed"""

    splitcontainer.direction = toga.SplitContainer.HORIZONTAL

    # The direction has been set
    assert splitcontainer.direction == toga.SplitContainer.HORIZONTAL

    # The scroll container has been refreshed
    assert_action_performed(splitcontainer, "refresh")
