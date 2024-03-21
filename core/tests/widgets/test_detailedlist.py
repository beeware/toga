from unittest.mock import Mock

import pytest

import toga
from toga.sources import ListSource
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)


@pytest.fixture
def on_select_handler():
    return Mock()


@pytest.fixture
def on_refresh_handler():
    return Mock(return_value=None)


@pytest.fixture
def on_primary_action_handler():
    return Mock()


@pytest.fixture
def on_secondary_action_handler():
    return Mock()


@pytest.fixture
def source():
    return ListSource(
        accessors=["key", "value", "icon"],
        data=[
            {"key": "first", "value": 111, "other": "aaa"},
            {"key": "second", "value": 222, "other": "bbb"},
            {"key": "third", "value": 333, "other": "ccc"},
        ],
    )


@pytest.fixture
def detailedlist(
    source,
    on_select_handler,
    on_refresh_handler,
    on_primary_action_handler,
    on_secondary_action_handler,
):
    return toga.DetailedList(
        accessors=["key", "value", "icon"],
        data=source,
        on_select=on_select_handler,
        on_refresh=on_refresh_handler,
        on_primary_action=on_primary_action_handler,
        on_secondary_action=on_secondary_action_handler,
    )


def test_detailedlist_created():
    """A minimal DetailedList can be created."""
    detailedlist = toga.DetailedList()
    assert detailedlist._impl.interface == detailedlist
    assert_action_performed(detailedlist, "create DetailedList")

    assert len(detailedlist.data) == 0
    assert detailedlist.accessors == ("title", "subtitle", "icon")
    assert detailedlist.missing_value == ""
    assert detailedlist.on_select._raw is None
    assert detailedlist.on_refresh._raw is None
    assert detailedlist.on_primary_action._raw is None
    assert detailedlist.on_secondary_action._raw is None
    assert detailedlist._primary_action == "Delete"
    assert detailedlist._secondary_action == "Action"

    assert_action_performed_with(detailedlist, "refresh enabled", enabled=False)
    assert_action_performed_with(detailedlist, "primary action enabled", enabled=False)
    assert_action_performed_with(
        detailedlist, "secondary action enabled", enabled=False
    )


def test_create_with_values(
    source,
    on_select_handler,
    on_refresh_handler,
    on_primary_action_handler,
    on_secondary_action_handler,
):
    """A DetailedList can be created with initial values."""
    detailedlist = toga.DetailedList(
        data=source,
        accessors=("key", "value", "icon"),
        missing_value="Boo!",
        on_select=on_select_handler,
        on_refresh=on_refresh_handler,
        primary_action="Primary",
        on_primary_action=on_primary_action_handler,
        secondary_action="Secondary",
        on_secondary_action=on_secondary_action_handler,
    )
    assert detailedlist._impl.interface == detailedlist
    assert_action_performed(detailedlist, "create DetailedList")

    assert len(detailedlist.data) == 3
    assert detailedlist.accessors == ("key", "value", "icon")
    assert detailedlist.missing_value == "Boo!"
    assert detailedlist.on_select._raw == on_select_handler
    assert detailedlist.on_refresh._raw == on_refresh_handler
    assert detailedlist.on_primary_action._raw == on_primary_action_handler
    assert detailedlist.on_secondary_action._raw == on_secondary_action_handler
    assert detailedlist._primary_action == "Primary"
    assert detailedlist._secondary_action == "Secondary"

    assert_action_performed_with(detailedlist, "refresh enabled", enabled=True)
    assert_action_performed_with(detailedlist, "primary action enabled", enabled=True)
    assert_action_performed_with(detailedlist, "secondary action enabled", enabled=True)


def test_disable_no_op(detailedlist):
    """DetailedList doesn't have a disabled state."""
    # Enabled by default
    assert detailedlist.enabled

    # Try to disable the widget
    detailedlist.enabled = False

    # Still enabled.
    assert detailedlist.enabled


def test_focus_noop(detailedlist):
    """Focus is a no-op."""

    detailedlist.focus()
    assert_action_not_performed(detailedlist, "focus")


@pytest.mark.parametrize(
    "data, all_attributes, extra_attributes",
    [
        # List of lists
        (
            [
                ["Alice", 123, "icon1"],
                ["Bob", 234, "icon2"],
                ["Charlie", 345, "icon3"],
            ],
            True,
            False,
        ),
        # List of tuples
        (
            [
                ("Alice", 123, "icon1"),
                ("Bob", 234, "icon2"),
                ("Charlie", 345, "icon3"),
            ],
            True,
            False,
        ),
        # List of dictionaries
        (
            [
                {"key": "Alice", "value": 123, "icon": "icon1", "extra": "extra1"},
                {"key": "Bob", "value": 234, "icon": "icon2", "extra": "extra2"},
                {"key": "Charlie", "value": 345, "icon": "icon3", "extra": "extra3"},
            ],
            True,
            True,
        ),
        # List of bare data
        (
            [
                "Alice",
                1234,
                "Charlie",
            ],
            False,
            False,
        ),
    ],
)
def test_set_data(
    detailedlist,
    on_select_handler,
    data,
    all_attributes,
    extra_attributes,
):
    """Data can be set from a variety of sources."""

    # The selection hasn't changed yet.
    on_select_handler.assert_not_called()

    # Change the data
    detailedlist.data = data

    # This triggered the select handler
    on_select_handler.assert_called_once_with(detailedlist)

    # A ListSource has been constructed
    assert isinstance(detailedlist.data, ListSource)
    assert len(detailedlist.data) == 3

    # The accessors are mapped in order.
    assert detailedlist.data[0].key == "Alice"
    assert detailedlist.data[2].key == "Charlie"

    if all_attributes:
        assert detailedlist.data[1].key == "Bob"

        assert detailedlist.data[0].value == 123
        assert detailedlist.data[1].value == 234
        assert detailedlist.data[2].value == 345

        assert detailedlist.data[0].icon == "icon1"
        assert detailedlist.data[1].icon == "icon2"
        assert detailedlist.data[2].icon == "icon3"
    else:
        assert detailedlist.data[1].key == 1234

    if extra_attributes:
        assert detailedlist.data[0].extra == "extra1"
        assert detailedlist.data[1].extra == "extra2"
        assert detailedlist.data[2].extra == "extra3"


def test_selection(detailedlist, on_select_handler):
    """The current selection can be retrieved."""
    # Selection is initially empty
    assert detailedlist.selection is None
    on_select_handler.assert_not_called()

    # Select an item
    detailedlist._impl.simulate_selection(1)

    # Selection returns a single row
    assert detailedlist.selection == detailedlist.data[1]

    # Selection handler was triggered
    on_select_handler.assert_called_once_with(detailedlist)


def test_refresh(detailedlist, on_refresh_handler):
    """Completion of a refresh event triggers the cleanup handler."""
    # Stimulate a refresh.
    detailedlist._impl.stimulate_refresh()

    # refresh handler was invoked
    on_refresh_handler.assert_called_once_with(detailedlist)

    # The post-refresh handler was invoked on the backend
    assert_action_performed_with(
        detailedlist,
        "after on refresh",
        widget=detailedlist,
        result=None,
    )


def test_scroll_to_top(detailedlist):
    """A DetailedList can be scrolled to the top."""
    detailedlist.scroll_to_top()

    assert_action_performed_with(detailedlist, "scroll to row", row=0)


@pytest.mark.parametrize(
    "row, effective",
    [
        # Positive index
        (0, 0),
        (2, 2),
        # Greater index than available rows
        (10, 3),
        # Negative index
        (-1, 2),
        (-3, 0),
        # Greater negative index than available rows
        (-10, 0),
    ],
)
def test_scroll_to_row(detailedlist, row, effective):
    """A DetailedList can be scrolled to a specific row."""
    detailedlist.scroll_to_row(row)

    assert_action_performed_with(detailedlist, "scroll to row", row=effective)


def test_scroll_to_row_no_data(detailedlist):
    """If there's no data, scrolling is a no-op."""
    detailedlist.data.clear()

    detailedlist.scroll_to_row(5)

    assert_action_not_performed(detailedlist, "scroll to row")


def test_scroll_to_bottom(detailedlist):
    """A DetailedList can be scrolled to the top."""
    detailedlist.scroll_to_bottom()

    assert_action_performed_with(detailedlist, "scroll to row", row=2)


######################################################################
# 2023-07: Backwards compatibility
######################################################################
def test_deprecated_names(on_primary_action_handler):
    """Deprecated names still work."""

    # Can't specify both on_delete and on_primary_action
    with pytest.raises(
        ValueError,
        match=r"Cannot specify both on_delete and on_primary_action",
    ):
        toga.DetailedList(on_delete=Mock(), on_primary_action=Mock())

    # on_delete is redirected at construction
    with pytest.warns(
        DeprecationWarning,
        match="DetailedList.on_delete has been renamed DetailedList.on_primary_action",
    ):
        select = toga.DetailedList(on_delete=on_primary_action_handler)

    # on_delete accessor is redirected to on_primary_action
    with pytest.warns(
        DeprecationWarning,
        match="DetailedList.on_delete has been renamed DetailedList.on_primary_action",
    ):
        assert select.on_delete._raw == on_primary_action_handler

    assert select.on_primary_action._raw == on_primary_action_handler

    # on_delete mutator is redirected to on_primary_action
    new_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match="DetailedList.on_delete has been renamed DetailedList.on_primary_action",
    ):
        select.on_delete = new_handler

    assert select.on_primary_action._raw == new_handler
