from unittest.mock import Mock

import pytest

import toga
from toga.sources import ListSource
from toga_dummy.utils import (
    EventLog,
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def on_change_handler():
    return Mock()


@pytest.fixture
def source():
    return ListSource(
        accessors=["key", "value"],
        data=[
            {"key": "first", "value": 111},
            {"key": "second", "value": 222},
            {"key": "third", "value": 333},
        ],
    )


@pytest.fixture
def widget(source, on_change_handler):
    return toga.Selection(
        accessor="key",
        items=source,
        value=source[1],
        on_change=on_change_handler,
    )


def test_widget_created():
    """An empty selection can be created."""
    widget = toga.Selection()
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create Selection")

    assert len(widget.items) == 0
    assert widget._accessor is None
    assert widget.value is None
    assert widget.on_change._raw is None
    assert widget.enabled


def test_create_with_value():
    """A Selection can be created with initial values."""
    on_change = Mock()

    widget = toga.Selection(
        items=["first", "second", "third"],
        value="second",
        on_change=on_change,
        enabled=False,
    )
    assert widget._impl.interface == widget
    assert_action_performed(widget, "create Selection")

    assert len(widget.items) == 3
    assert widget._accessor is None
    assert widget.value == "second"
    assert widget.on_change._raw == on_change
    assert not widget.enabled


@pytest.mark.parametrize(
    "items, title, value",
    [
        # list of strings
        (["first", "second", "third"], "second", "second"),
        # list of non-strings
        ([111, 222, 333], "222", 222),
        # List of dictionaries; implied use of "value" key
        (
            [
                {"key": "first", "value": 111},
                {"key": "second", "value": 222},
                {"key": "third", "value": 333},
            ],
            "222",
            222,
        ),
        # List of tuples; only the first item is used.
        (
            [
                ("first", 111),
                ("second", 222),
                ("third", 333),
            ],
            "second",
            "second",
        ),
        # List of strings with a newline in value
        (["first", "second\nitem", "third"], "second", "second\nitem"),
        # List of strings with a duplicate entry
        (["first", "second", "third", "first", "second"], "second", "second"),
    ],
)
def test_value_no_accessor(items, title, value):
    """If there's no accessor, the items can be set and values will be dereferenced."""
    on_change_handler = Mock()
    widget = toga.Selection(on_change=on_change_handler)

    # There haven't been any changes
    on_change_handler.assert_not_called()

    # Change the items. This changes the selection, triggering the handler
    widget.items = items

    on_change_handler.assert_called_once_with(widget)

    # Default selection is the first item
    # As there's no accessor, the value auto-dereferences
    assert widget.value == widget.items[0].value

    # Reset the mock
    on_change_handler.reset_mock()

    # Change the value
    widget.value = value
    assert widget.value == value

    # The value renders as a string
    assert widget._title_for_item(widget.items[1]) == title

    # Change handler was invoked
    on_change_handler.assert_called_once_with(widget)


@pytest.mark.parametrize(
    "accessor, items, title, value",
    [
        # List of strings with a custom accessor name
        ("key", ["first", "second", "third"], "second", "second"),
        # List of dictionaries selecting non-default key
        (
            "key",
            [
                {"key": "first", "value": 111},
                {"key": "second", "value": 222},
                {"key": "third", "value": 333},
            ],
            "second",
            "second",
        ),
        # List of tuples; accessor name is altered.
        (
            "key",
            [
                ("first", 111),
                ("second", 222),
                ("third", 333),
            ],
            "second",
            "second",
        ),
        (
            "key",
            ListSource(
                accessors=["key", "value"],
                data=[
                    {"key": "first", "value": 111},
                    {"key": "second", "value": 222},
                    {"key": "third", "value": 333},
                ],
            ),
            "second",
            "second",
        ),
        # List of strings with a newline in a title
        ("key", ["first", "second\nitem", "third"], "second", "second\nitem"),
        # List of strings with a duplicate entry
        ("key", ["first", "second", "third", "first", "second"], "second", "second"),
    ],
)
def test_value_with_accessor(accessor, items, title, value):
    """If an accessor is used, item lookup semantics are different."""
    on_change_handler = Mock()
    widget = toga.Selection(accessor=accessor, on_change=on_change_handler)

    # There haven't been any changes
    on_change_handler.assert_not_called()

    # Change the items. This changes the selection, triggering the handler
    widget.items = items

    on_change_handler.assert_called_once_with(widget)

    # Default selection is the first item
    # As there is an accessor, we get back a literal row object.
    assert widget.value == widget.items[0]

    # Reset the mock
    on_change_handler.reset_mock()

    # Change the value. As there is an accessor, we use a literal row object,
    # and need to manually access attributes on that row.
    widget.value = widget.items[1]
    assert getattr(widget.value, accessor) == value

    # The value renders as a string
    assert widget._title_for_item(widget.items[1]) == title

    # Change handler was invoked
    on_change_handler.assert_called_once_with(widget)


def test_source_no_accessor():
    """If the selection is based on a source, it must specify an accessor."""
    with pytest.raises(
        ValueError,
        match=r"Must specify an accessor to use a data source",
    ):
        toga.Selection(items=ListSource(accessors=["foo", "bar"]))


def test_bad_item_no_accessor():
    """The value for the selection must exist in accessor-less data."""
    selection = toga.Selection(items=["first", "second", "third"])

    with pytest.raises(
        ValueError,
        match=r"'bad' is not a current item in the selection",
    ):
        selection.value = "bad"


def test_bad_item_with_accessor():
    """The value for the selection must exist in accessor-based data."""
    # Create a selection with an extra item and an explicit accessor
    selection = toga.Selection(
        accessor="value", items=["first", "bad", "second", "third"]
    )

    # Store the bad item
    item = selection.items.find(dict(value="bad"))

    # Delete the bad item
    selection.items.remove(item)

    # item is no longer a valid selection
    with pytest.raises(
        ValueError,
        match=r"<Row .* value='bad'> is not a current item in the selection",
    ):
        selection.value = item


def test_add_item(widget, source, on_change_handler):
    """A row can be added to the source."""
    # Store the original selection
    selection = widget.value

    source.append(dict(key="new", value=999))

    # The widget adds the item
    assert_action_performed_with(widget, "insert item", index=3)

    # This doesn't change the widget.
    on_change_handler.assert_not_called()
    assert widget.value == selection


def test_insert_item(widget, source, on_change_handler):
    """A row can be inserted into the source."""
    # Store the original selection
    selection = widget.value

    source.insert(1, dict(key="new", value=999))

    # The widget adds the item
    assert_action_performed_with(widget, "insert item", index=1)

    # This doesn't change the widget
    on_change_handler.assert_not_called()
    assert widget.value == selection


def test_remove(widget, source, on_change_handler):
    """If you remove an item that isn't selected, no change is generated."""
    # Store the original selection
    selection = widget.value

    # Remove a non-selected item
    item = source[0]
    source.remove(item)

    # The widget adds the item
    assert_action_performed_with(widget, "remove item", index=0, item=item)

    # This changes the selection
    on_change_handler.assert_not_called()
    assert widget.value == selection


def test_remove_selected(widget, source, on_change_handler):
    """If you remove the currently selected item, a change is generated."""
    # Store the original selection
    selection = widget.value

    source.remove(selection)

    # The widget adds the item
    assert_action_performed_with(widget, "remove item", index=1, item=selection)

    # This changes the selection
    on_change_handler.assert_called_with(widget)
    assert widget.value == source[0]


def test_clear_source(widget, source, on_change_handler):
    """If the source is cleared, the selection is cleared."""
    # Clear the source
    source.clear()

    # The widget has been cleared
    assert_action_performed(widget, "clear")

    # The widget must have cleared its selection
    on_change_handler.assert_called_with(widget)
    assert widget.value is None


def test_change_source_empty(widget, on_change_handler):
    """If the source is changed to an empty source, the selection is reset."""
    # Clear the event history
    EventLog.reset()

    widget.items = []

    # The widget data has been cleared and refreshed
    assert_action_performed(widget, "clear")
    assert_action_not_performed(widget, "insert item")
    assert_action_performed(widget, "refresh")

    # The widget must have cleared its selection
    on_change_handler.assert_called_once_with(widget)
    assert widget.value is None


def test_change_source(widget, on_change_handler):
    """If the source is changed, the selection is set to the first item."""
    # Clear the event history
    EventLog.reset()

    # Change the source of the data
    widget.items = ["new 1", "new 2"]

    # The widget source has changed
    assert_action_performed(widget, "clear")
    assert_action_performed_with(widget, "insert item", item=widget.items[0])
    assert_action_performed_with(widget, "insert item", item=widget.items[1])
    assert_action_performed(widget, "refresh")

    # The widget must have cleared its selection
    on_change_handler.assert_called_once_with(widget)
    assert widget.value.key == "new 1"


######################################################################
# 2023-05: Backwards compatibility
######################################################################


def test_deprecated_names(on_change_handler):
    """Deprecated names still work."""

    # Can't specify both on_select and on_change
    with pytest.raises(
        ValueError,
        match=r"Cannot specify both on_select and on_change",
    ):
        toga.Selection(on_select=Mock(), on_change=Mock())

    # on_select is redirected at construction
    with pytest.warns(
        DeprecationWarning,
        match="Selection.on_select has been renamed Selection.on_change",
    ):
        select = toga.Selection(on_select=on_change_handler)

    # on_select accessor is redirected to on_change
    with pytest.warns(
        DeprecationWarning,
        match="Selection.on_select has been renamed Selection.on_change",
    ):
        assert select.on_select._raw == on_change_handler

    assert select.on_change._raw == on_change_handler

    # on_select mutator is redirected to on_change
    new_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match="Selection.on_select has been renamed Selection.on_change",
    ):
        select.on_select = new_handler

    assert select.on_change._raw == new_handler
