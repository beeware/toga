from unittest.mock import Mock

import pytest

import toga
from toga_dummy import factory as dummy_factory
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


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
def content4():
    return toga.Box()


@pytest.fixture
def on_select_handler():
    return Mock()


@pytest.fixture
def tab_icon(app):
    return toga.Icon("tab-icon")


@pytest.fixture
def optioncontainer(
    content1,
    content2,
    content3,
    content4,
    on_select_handler,
    tab_icon,
):
    return toga.OptionContainer(
        content=[
            ("Item 1", content1),
            ("Item 2", content2, "other-icon"),
            ("Item 3", content3, tab_icon, False),
            toga.OptionItem("Item 4", content4),
        ],
        on_select=on_select_handler,
    )


def test_widget_create():
    """An option container can be created with no arguments."""
    optioncontainer = toga.OptionContainer()
    assert_action_performed(optioncontainer, "create OptionContainer")

    assert len(optioncontainer.content) == 0
    assert optioncontainer.current_tab is None
    assert optioncontainer.on_select._raw is None


def test_widget_create_with_args(
    optioncontainer,
    content1,
    content2,
    content3,
    content4,
    on_select_handler,
    tab_icon,
):
    """An option container can be created with arguments."""
    assert optioncontainer._impl.interface == optioncontainer
    assert_action_performed(optioncontainer, "create OptionContainer")

    assert len(optioncontainer.content) == 4
    assert optioncontainer.current_tab.text == "Item 1"
    assert optioncontainer.current_tab.icon is None
    assert optioncontainer.current_tab.enabled
    assert optioncontainer.current_tab.content == content1
    assert optioncontainer.on_select._raw == on_select_handler

    assert optioncontainer.content[1].text == "Item 2"
    assert optioncontainer.content[1].icon.path.name == "other-icon"
    assert optioncontainer.content[1].content == content2
    assert optioncontainer.content[1].enabled

    assert optioncontainer.content[2].text == "Item 3"
    assert optioncontainer.content[2].icon == tab_icon
    assert optioncontainer.content[2].content == content3
    assert not optioncontainer.content[2].enabled

    assert optioncontainer.content[3].text == "Item 4"
    assert optioncontainer.content[3].icon is None
    assert optioncontainer.content[3].content == content4
    assert optioncontainer.content[3].enabled


@pytest.mark.parametrize(
    "value",
    [
        ("label",),
        ("label", toga.Box(), None, True, "extra"),
    ],
)
def test_widget_create_invalid_content(value):
    """If the content provided at construction isn't 2- or 3-tuples, an error is
    raised."""
    with pytest.raises(
        ValueError,
        match=(
            r"Content items must be an OptionItem instance, or tuples of \(title, widget\), "
            r"\(title, widget, icon\), or \(title, widget, icon, enabled\)"
        ),
    ):
        toga.OptionContainer(content=value)


def test_item_create(content1):
    """An OptionItem can be created."""
    item = toga.OptionItem("label", content1)

    assert item.text == "label"
    assert item.content == content1
    assert item.index is None
    assert item.interface is None


@pytest.mark.parametrize(
    "title, has_content, has_icon, enabled, message",
    [
        (None, True, True, True, r"Item text cannot be None"),
        ("", True, True, True, r"Item text cannot be blank"),
        ("label", False, True, True, r"Content widget cannot be None"),
    ],
)
def test_item_create_invalid_item(
    title,
    has_content,
    has_icon,
    enabled,
    message,
    content1,
    tab_icon,
):
    """If item details are invalid, an exception is raised."""

    with pytest.raises(ValueError, match=message):
        toga.OptionItem(
            title,
            content1 if has_content else None,
            icon=tab_icon if has_icon else None,
            enabled=enabled,
        )


def test_assign_to_app(app, optioncontainer, content1, content2, content3):
    """If the widget is assigned to an app, the content is also assigned."""
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
    """If the widget is assigned to an app, and there is no content, there's no
    error."""
    optioncontainer = toga.OptionContainer()

    # Option container is initially unassigned
    assert optioncontainer.app is None

    # Assign the Option container to the app
    optioncontainer.app = app

    # Option container is on the app
    assert optioncontainer.app == app


def test_assign_to_window(window, optioncontainer, content1, content2, content3):
    """If the widget is assigned to a window, the content is also assigned."""
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
    """If the widget is assigned to a window, and there is no content, there's no
    error."""
    optioncontainer = toga.OptionContainer()

    # Option container is initially unassigned
    assert optioncontainer.window is None

    # Assign the Option container to the window
    optioncontainer.window = window

    # Option container is on the window
    assert optioncontainer.window == window


def test_disable_no_op(optioncontainer):
    """OptionContainer doesn't have a disabled state."""
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


@pytest.mark.parametrize("bare_item", [True, False])
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
def test_item_enabled(optioncontainer, value, expected, bare_item):
    """The enabled status of an item can be changed."""
    if bare_item:
        item = toga.OptionItem("title", toga.Box())
    else:
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
    """The currently selected item cannot be disabled."""
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


@pytest.mark.parametrize("bare_item", [True, False])
@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Title", "New Title"),
        (42, "42"),  # Evaluated as a string
        (MyTitle("Custom Title"), "Custom Title"),  # Evaluated as a string
    ],
)
def test_item_text(optioncontainer, value, expected, bare_item):
    """The title of an item can be changed."""
    if bare_item:
        item = toga.OptionItem("title", toga.Box())
    else:
        item = optioncontainer.content[1]

    # Set the item text
    item.text = value
    assert item.text == expected


@pytest.mark.parametrize("bare_item", [True, False])
@pytest.mark.parametrize(
    "value, error",
    [
        (None, r"Item text cannot be None"),
        ("", r"Item text cannot be blank"),
        (MyTitle(""), r"Item text cannot be blank"),
    ],
)
def test_invalid_item_text(optioncontainer, value, error, bare_item):
    """Invalid item titles are prevented."""
    if bare_item:
        item = toga.OptionItem("title", toga.Box())
    else:
        item = optioncontainer.content[1]

    # Using invalid text raises an error
    with pytest.raises(ValueError, match=error):
        item.text = value


@pytest.mark.parametrize("bare_item", [True, False])
def test_item_icon(optioncontainer, bare_item):
    """The icon of an item can be changed."""
    if bare_item:
        item = toga.OptionItem("title", toga.Box())
    else:
        item = optioncontainer.content[0]

    # Icon is initially empty
    assert item.icon is None

    test_icon = toga.Icon("test-icon")
    item.icon = test_icon

    # Icon has been set
    assert item.icon == test_icon
    if bare_item:
        assert_action_not_performed(optioncontainer, "set option icon")
    else:
        assert_action_performed_with(
            optioncontainer,
            "set option icon",
            index=0,
        )
    EventLog.reset()

    # Clear the icon
    item.icon = None

    # Icon has been reset
    assert item.icon is None
    if bare_item:
        assert_action_not_performed(optioncontainer, "set option icon")
    else:
        assert_action_performed_with(
            optioncontainer,
            "set option icon",
            index=0,
            icon=None,
        )
    EventLog.reset()

    # Icon has been set by name
    item.icon = "new-icon"

    # Icon has been set to the new value
    assert item.icon.path.name == "new-icon"
    if bare_item:
        assert_action_not_performed(optioncontainer, "set option icon")
    else:
        assert_action_performed_with(
            optioncontainer,
            "set option icon",
            index=0,
        )


@pytest.mark.parametrize("bare_item", [True, False])
def test_item_icon_disabled(monkeypatch, optioncontainer, bare_item):
    """The icon of an item won't be set if icons aren't in use."""
    # monkeypatch the OptionContainer class to disable the use of icons
    monkeypatch.setattr(dummy_factory.OptionContainer, "uses_icons", False)

    if bare_item:
        item = toga.OptionItem("title", toga.Box())
    else:
        item = optioncontainer.content[0]

    # Icon is initially empty
    assert item.icon is None

    # Try to set an icon
    item.icon = "test-icon"

    # Icon is still none
    assert item.icon is None

    # Add a new content item with an icon
    optioncontainer.content.append("New content", toga.Box(), icon="new-icon")

    # Icon is still none
    assert optioncontainer.content["New content"].icon is None


def test_optionlist_repr(optioncontainer):
    """OptionContainer content has a helpful repr."""
    assert (
        repr(optioncontainer.content)
        == "<OptionList 'Item 1', 'Item 2', 'Item 3', 'Item 4'>"
    )


def test_optionlist_iter(optioncontainer):
    """OptionContainer content can be iterated."""
    assert [item.text for item in optioncontainer.content] == [
        "Item 1",
        "Item 2",
        "Item 3",
        "Item 4",
    ]


def test_optionlist_len(optioncontainer):
    """OptionContainer content has length."""
    assert len(optioncontainer.content) == 4


@pytest.mark.parametrize("index", [1, "Item 2", None])
def test_getitem(optioncontainer, content2, index):
    """An item can be retrieved."""
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
    assert len(optioncontainer.content) == 3
    assert_action_performed_with(optioncontainer, "remove option", index=1)

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
    """The current item can't be deleted."""
    if index is None:
        index = optioncontainer.content[0]

    with pytest.raises(
        ValueError, match=r"The currently selected tab cannot be deleted."
    ):
        del optioncontainer.content[index]


@pytest.mark.parametrize("index", [1, "Item 2", None])
def test_item_remove(optioncontainer, index):
    """An item can be removed with remove."""
    if index is None:
        index = optioncontainer.content[1]

    # get a reference to items 1 and 3
    item1 = optioncontainer.content[0]
    item3 = optioncontainer.content[2]

    # remove item
    optioncontainer.content.remove(index)
    assert len(optioncontainer.content) == 3
    assert_action_performed_with(optioncontainer, "remove option", index=1)

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
    """The current item can't be removed."""
    if index is None:
        index = optioncontainer.content[0]

    with pytest.raises(
        ValueError, match=r"The currently selected tab cannot be deleted."
    ):
        optioncontainer.content.remove(index)


def test_item_insert_item(optioncontainer):
    """The text of an inserted item can be set."""
    new_content = toga.Box()
    item = toga.OptionItem("New Tab", new_content)

    optioncontainer.content.insert(1, item)

    # Backend added an item and set enabled
    assert_action_performed_with(
        optioncontainer,
        "add option",
        index=1,
        text="New Tab",
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
    "args,kwargs,message",
    [
        (
            ("New Tab",),
            {},
            r"Content widget cannot be None.",
        ),
        (
            (toga.OptionItem("New Tab", toga.Box()),),
            {"content": toga.Box()},
            r"Cannot specify content if using an OptionItem instance.",
        ),
        (
            (toga.OptionItem("New Tab", toga.Box()),),
            {"icon": "tab-icon"},
            r"Cannot specify icon if using an OptionItem instance.",
        ),
        (
            (toga.OptionItem("New Tab", toga.Box()),),
            {"enabled": False},
            r"Cannot specify enabled if using an OptionItem instance.",
        ),
    ],
)
def test_item_insert_item_invalid(optioncontainer, args, kwargs, message):
    """If both an item and specific details are provided, an error is raised."""
    with pytest.raises(ValueError, match=message):
        optioncontainer.content.insert(1, *args, **kwargs)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Title", "New Title"),
        (42, "42"),  # Evaluated as a string
        (MyTitle("Custom Title"), "Custom Title"),  # Evaluated as a string
    ],
)
def test_item_insert_text(optioncontainer, value, expected):
    """The text of an inserted item can be set."""
    new_content = toga.Box()

    optioncontainer.content.insert(1, value, new_content, enabled=True)

    # Backend added an item and set enabled
    assert_action_performed_with(
        optioncontainer,
        "add option",
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
    """The item text must be valid."""
    new_content = toga.Box()
    with pytest.raises(ValueError, match=error):
        optioncontainer.content.insert(1, value, new_content, enabled=True)


@pytest.mark.parametrize("enabled", [True, False])
def test_item_insert_enabled(optioncontainer, enabled):
    """The enabled status of content can be set on insert."""
    new_content = toga.Box()

    optioncontainer.content.insert(1, "New content", new_content, enabled=enabled)

    # Backend added an item and set enabled
    assert_action_performed_with(
        optioncontainer,
        "add option",
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
    """An item can be appended to the content list."""
    # append is implemented using insert;
    # the bulk of the functionality is tested there.
    new_content = toga.Box()

    optioncontainer.content.append("New content", new_content, enabled=enabled)
    assert_action_performed_with(
        optioncontainer, "add option", index=4, widget=new_content._impl
    )
    assert_action_performed_with(
        optioncontainer, "set option enabled", index=4, value=enabled
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
