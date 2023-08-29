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
    return toga.App("Option Container Test", "org.beeware.toga.option_container")


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
def on_select_handler():
    return Mock()


@pytest.fixture
def optioncontainer(content1, content2, content3, on_select_handler):
    return toga.OptionContainer(
        content=[("Item 1", content1), ("Item 2", content2), ("Item 3", content3)],
        on_select=on_select_handler,
    )


def test_widget_create():
    "An option container can be created with no arguments"
    optioncontainer = toga.OptionContainer()
    assert_action_performed(optioncontainer, "create OptionContainer")

    assert len(optioncontainer.content) == 0
    assert optioncontainer.current_tab is None
    assert optioncontainer.on_select._raw is None


def test_widget_create_with_args(optioncontainer, on_select_handler):
    "An option container can be created with arguments"
    assert optioncontainer._impl.interface == optioncontainer
    assert_action_performed(optioncontainer, "create OptionContainer")

    assert len(optioncontainer.content) == 3
    assert optioncontainer.current_tab.text == "Item 1"
    assert optioncontainer.on_select._raw == on_select_handler


def test_assign_to_app(app, optioncontainer, content1, content2, content3):
    """If the widget is assigned to an app, the content is also assigned"""
    # Option container is initially unassigned
    assert optioncontainer.app is None

    # Assign the option container to the app
    optioncontainer.app = app

    # option container is on the app
    assert optioncontainer.app == app

    # Content is also on the app
    assert content1.app == app
    assert content2.app == app
    assert content3.app == app


def test_assign_to_app_no_content(app):
    """If the widget is assigned to an app, and there is no content, there's no error"""
    optioncontainer = toga.OptionContainer()

    # Option container is initially unassigned
    assert optioncontainer.app is None

    # Assign the Option container to the app
    optioncontainer.app = app

    # Option container is on the app
    assert optioncontainer.app == app


def test_assign_to_window(window, optioncontainer, content1, content2, content3):
    """If the widget is assigned to a window, the content is also assigned"""
    # Option container is initially unassigned
    assert optioncontainer.window is None

    # Assign the Option container to the window
    optioncontainer.window = window

    # Option container is on the window
    assert optioncontainer.window == window
    # Content is also on the window
    assert content1.window == window
    assert content2.window == window
    assert content3.window == window


def test_assign_to_window_no_content(window):
    """If the widget is assigned to a window, and there is no content, there's no error"""
    optioncontainer = toga.OptionContainer()

    # Option container is initially unassigned
    assert optioncontainer.window is None

    # Assign the Option container to the window
    optioncontainer.window = window

    # Option container is on the window
    assert optioncontainer.window == window


def test_disable_no_op(optioncontainer):
    """OptionContainer doesn't have a disabled state"""
    # Enabled by default
    assert optioncontainer.enabled

    # Try to disable the widget
    optioncontainer.enabled = False

    # Still enabled.
    assert optioncontainer.enabled


def test_focus_noop(optioncontainer):
    """Focus is a no-op."""

    optioncontainer.focus()
    assert_action_not_performed(optioncontainer, "focus")


@pytest.mark.parametrize(
    "value, expected",
    [
        (None, False),
        ("", False),
        ("true", True),
        ("false", True),  # Evaluated as a string, this value is true.
        (0, False),
        (1234, True),
    ],
)
def test_item_enabled(optioncontainer, value, expected):
    """The enabled status of an item can be changed."""
    item = optioncontainer.content[1]

    # item is initially enabled by default.
    assert item.enabled

    # Set the enabled status
    item.enabled = value
    assert item.enabled == expected

    # Disable the widget
    item.enabled = False
    assert not item.enabled

    # Set the enabled status again
    item.enabled = value
    assert item.enabled == expected


def test_disable_current_item(optioncontainer):
    """The currently selected item cannot be disabled"""
    # Item 0 is selected by default
    item = optioncontainer.content[0]
    with pytest.raises(
        ValueError,
        match=r"The currently selected tab cannot be disabled.",
    ):
        item.enabled = False

    # Try disabling the current tab directly
    with pytest.raises(
        ValueError,
        match=r"The currently selected tab cannot be disabled.",
    ):
        optioncontainer.current_tab.enabled = False


class MyTitle:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Title", "New Title"),
        (42, "42"),  # Evaluated as a string
        (MyTitle("Custom Title"), "Custom Title"),  # Evaluated as a string
    ],
)
def test_item_text(optioncontainer, value, expected):
    """The title of an item can be changed."""
    item = optioncontainer.content[1]

    # Set the item text
    item.text = value
    assert item.text == expected


@pytest.mark.parametrize(
    "value, error",
    [
        (None, r"Item text cannot be None"),
        ("", r"Item text cannot be blank"),
        (MyTitle(""), r"Item text cannot be blank"),
    ],
)
def test_invalid_item_text(optioncontainer, value, error):
    """Invalid item titles are prevented"""
    item = optioncontainer.content[1]

    # Using invalid text raises an error
    with pytest.raises(ValueError, match=error):
        item.text = value


def test_optionlist_repr(optioncontainer):
    """OptionContainer content has a helpful repr"""
    assert repr(optioncontainer.content) == "<OptionList 'Item 1', 'Item 2', 'Item 3'>"


def test_optionlist_iter(optioncontainer):
    """OptionContainer content can be iterated"""
    assert [item.text for item in optioncontainer.content] == [
        "Item 1",
        "Item 2",
        "Item 3",
    ]


def test_optionlist_len(optioncontainer):
    """OptionContainer content has length"""
    assert len(optioncontainer.content) == 3


@pytest.mark.parametrize("index", [1, "Item 2", None])
def test_getitem(optioncontainer, content2, index):
    """An item can be retrieved"""
    if index is None:
        index = optioncontainer.content[1]

    # get item
    item = optioncontainer.content[index]
    assert item.text == "Item 2"
    assert item.index == 1
    assert item.content == content2


@pytest.mark.parametrize("index", [1, "Item 2", None])
def test_delitem(optioncontainer, index):
    """An item can be removed with __del__"""
    if index is None:
        index = optioncontainer.content[1]

    # get a reference to items 1 and 3
    item1 = optioncontainer.content[0]
    item3 = optioncontainer.content[2]

    # delete item
    del optioncontainer.content[index]
    assert len(optioncontainer.content) == 2
    assert_action_performed_with(optioncontainer, "remove content", index=1)

    # There's no item with the deleted label
    with pytest.raises(ValueError, match=r"No tab named 'Item 2'"):
        optioncontainer.content.index("Item 2")

    # The index of item 3 has been reduced; item 1 is untouched
    assert item1.index == 0
    assert item3.index == 1

    # Widget has been refreshed
    assert_action_performed(optioncontainer, "refresh")


@pytest.mark.parametrize("index", [0, "Item 1", None])
def test_delitem_current(optioncontainer, index):
    """The current item can't be deleted"""
    if index is None:
        index = optioncontainer.content[0]

    with pytest.raises(
        ValueError, match=r"The currently selected tab cannot be deleted."
    ):
        del optioncontainer.content[index]


@pytest.mark.parametrize("index", [1, "Item 2", None])
def test_item_remove(optioncontainer, index):
    """An item can be removed with remove"""
    if index is None:
        index = optioncontainer.content[1]

    # get a reference to items 1 and 3
    item1 = optioncontainer.content[0]
    item3 = optioncontainer.content[2]

    # remove item
    optioncontainer.content.remove(index)
    assert len(optioncontainer.content) == 2
    assert_action_performed_with(optioncontainer, "remove content", index=1)

    # There's no item with the deleted label
    with pytest.raises(ValueError, match=r"No tab named 'Item 2'"):
        optioncontainer.content.index("Item 2")

    # The index of item 3 has been reduced; item 1 is untouched
    assert item1.index == 0
    assert item3.index == 1

    # Widget has been refreshed
    assert_action_performed(optioncontainer, "refresh")


@pytest.mark.parametrize("index", [0, "Item 1", None])
def test_item_remove_current(optioncontainer, index):
    """The current item can't be removed"""
    if index is None:
        index = optioncontainer.content[0]

    with pytest.raises(
        ValueError, match=r"The currently selected tab cannot be deleted."
    ):
        optioncontainer.content.remove(index)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Title", "New Title"),
        (42, "42"),  # Evaluated as a string
        (MyTitle("Custom Title"), "Custom Title"),  # Evaluated as a string
    ],
)
def test_item_insert_text(optioncontainer, value, expected):
    """The text of an inserted item can be set"""
    new_content = toga.Box()

    optioncontainer.content.insert(1, value, new_content, enabled=True)

    # Backend added an item and set enabled
    assert_action_performed_with(
        optioncontainer,
        "add content",
        index=1,
        text=expected,
        widget=new_content._impl,
    )
    assert_action_performed_with(
        optioncontainer,
        "set option enabled",
        index=1,
        value=True,
    )
    assert_action_performed_with(optioncontainer, "refresh")


@pytest.mark.parametrize(
    "value, error",
    [
        (None, r"Item text cannot be None"),
        ("", r"Item text cannot be blank"),
        (MyTitle(""), r"Item text cannot be blank"),
    ],
)
def test_item_insert_invalid_text(optioncontainer, value, error):
    """The item text must be valid"""
    new_content = toga.Box()
    with pytest.raises(ValueError, match=error):
        optioncontainer.content.insert(1, value, new_content, enabled=True)


@pytest.mark.parametrize("enabled", [True, False])
def test_item_insert_enabled(optioncontainer, enabled):
    """The enabled status of content can be set"""
    new_content = toga.Box()

    optioncontainer.content.insert(1, "New content", new_content, enabled=enabled)

    # Backend added an item and set enabled
    assert_action_performed_with(
        optioncontainer,
        "add content",
        index=1,
        text="New content",
        widget=new_content._impl,
    )
    assert_action_performed_with(
        optioncontainer,
        "set option enabled",
        index=1,
        value=enabled,
    )
    assert_action_performed_with(optioncontainer, "refresh")


@pytest.mark.parametrize("enabled", [True, False])
def test_item_append(optioncontainer, enabled):
    """An item can be appended to the content list"""
    # append is implemented using insert;
    # the bulk of the functionality is tested there.
    new_content = toga.Box()

    optioncontainer.content.append("New content", new_content, enabled=enabled)
    assert_action_performed_with(
        optioncontainer, "add content", index=3, widget=new_content._impl
    )
    assert_action_performed_with(
        optioncontainer, "set option enabled", index=3, value=enabled
    )
    assert_action_performed_with(optioncontainer, "refresh")


@pytest.mark.parametrize("index", [1, "Item 2", None])
def test_current_tab(optioncontainer, index, on_select_handler):
    """The current tab of the optioncontainer can be changed."""
    if index is None:
        index = optioncontainer.content[1]

    # First item is selected initially
    assert optioncontainer.current_tab.index == 0
    assert optioncontainer.current_tab.text == "Item 1"

    # Programmatically select item 2
    optioncontainer.current_tab = index

    # Current tab values have changed
    assert optioncontainer.current_tab.index == 1
    assert optioncontainer.current_tab.text == "Item 2"

    # on_select handler was invoked
    on_select_handler.assert_called_once_with(optioncontainer)


def test_select_disabled_tab(optioncontainer):
    """A disabled tab cannot be selected."""

    # Disable item 1
    item = optioncontainer.content[1]
    item.enabled = False

    with pytest.raises(
        ValueError,
        match=r"A disabled tab cannot be made the current tab.",
    ):
        optioncontainer.current_tab = 1
