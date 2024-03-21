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
def on_activate_handler():
    return Mock()


@pytest.fixture
def source():
    return ListSource(
        accessors=["key", "value"],
        data=[
            {"key": "first", "value": 111, "other": "aaa"},
            {"key": "second", "value": 222, "other": "bbb"},
            {"key": "third", "value": 333, "other": "ccc"},
        ],
    )


@pytest.fixture
def table(source, on_select_handler, on_activate_handler):
    return toga.Table(
        ["Title", "Value"],
        accessors=["key", "value"],
        data=source,
        on_select=on_select_handler,
        on_activate=on_activate_handler,
    )


def test_table_created():
    """A minimal Table can be created."""
    table = toga.Table(["First", "Second"])
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["First", "Second"]
    assert table.accessors == ["first", "second"]
    assert not table.multiple_select
    assert table.missing_value == ""
    assert table.on_select._raw is None
    assert table.on_activate._raw is None


def test_create_with_values(source, on_select_handler, on_activate_handler):
    """A Table can be created with initial values."""
    table = toga.Table(
        ["First", "Second"],
        data=source,
        accessors=["primus", "secondus"],
        multiple_select=True,
        on_select=on_select_handler,
        on_activate=on_activate_handler,
        missing_value="Boo!",
    )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 3
    assert table.headings == ["First", "Second"]
    assert table.accessors == ["primus", "secondus"]
    assert table.multiple_select
    assert table.missing_value == "Boo!"
    assert table.on_select._raw == on_select_handler
    assert table.on_activate._raw == on_activate_handler


def test_create_with_accessor_overrides():
    """A Table can partially override accessors."""
    table = toga.Table(
        ["First", "Second"],
        accessors={"First": "override"},
    )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["First", "Second"]
    assert table.accessors == ["override", "second"]


def test_create_no_headings():
    """A Table can be created with no headings."""
    table = toga.Table(
        headings=None,
        accessors=["primus", "secondus"],
    )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings is None
    assert table.accessors == ["primus", "secondus"]


def test_create_headings_required():
    """A Table requires either headings can be created with no headings."""
    with pytest.raises(
        ValueError,
        match=r"Cannot create a table without either headings or accessors",
    ):
        toga.Table()


def test_disable_no_op(table):
    """Table doesn't have a disabled state."""
    # Enabled by default
    assert table.enabled

    # Try to disable the widget
    table.enabled = False

    # Still enabled.
    assert table.enabled


def test_focus_noop(table):
    """Focus is a no-op."""

    table.focus()
    assert_action_not_performed(table, "focus")


@pytest.mark.parametrize(
    "data, all_attributes, extra_attributes",
    [
        # List of lists
        (
            [
                ["Alice", 123, "extra1"],
                ["Bob", 234, "extra2"],
                ["Charlie", 345, "extra3"],
            ],
            True,
            False,
        ),
        # List of tuples
        (
            [
                ("Alice", 123, "extra1"),
                ("Bob", 234, "extra2"),
                ("Charlie", 345, "extra3"),
            ],
            True,
            False,
        ),
        # List of dictionaries
        (
            [
                {"key": "Alice", "value": 123, "extra": "extra1"},
                {"key": "Bob", "value": 234, "extra": "extra2"},
                {"key": "Charlie", "value": 345, "extra": "extra3"},
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
def test_set_data(table, on_select_handler, data, all_attributes, extra_attributes):
    """Data can be set from a variety of sources."""

    # The selection hasn't changed yet.
    on_select_handler.assert_not_called()

    # Change the data
    table.data = data

    # This triggered the select handler
    on_select_handler.assert_called_once_with(table)

    # A ListSource has been constructed
    assert isinstance(table.data, ListSource)
    assert len(table.data) == 3

    # The accessors are mapped in order.
    assert table.data[0].key == "Alice"
    assert table.data[2].key == "Charlie"

    if all_attributes:
        assert table.data[1].key == "Bob"
        assert table.data[0].value == 123
        assert table.data[1].value == 234
        assert table.data[2].value == 345
    else:
        assert table.data[1].key == 1234

    if extra_attributes:
        assert table.data[0].extra == "extra1"
        assert table.data[1].extra == "extra2"
        assert table.data[2].extra == "extra3"


def test_single_selection(table, on_select_handler):
    """The current selection can be retrieved."""
    # Selection is initially empty
    assert table.selection is None
    on_select_handler.assert_not_called()

    # Select an item
    table._impl.simulate_selection(1)

    # Selection returns a single row
    assert table.selection == table.data[1]

    # Selection handler was triggered
    on_select_handler.assert_called_once_with(table)


def test_multiple_selection(source, on_select_handler):
    """A multi-select table can have the selection retrieved."""
    table = toga.Table(
        ["Title", "Value"],
        data=source,
        multiple_select=True,
        on_select=on_select_handler,
    )
    # Selection is initially empty
    assert table.selection == []
    on_select_handler.assert_not_called()

    # Select an item
    table._impl.simulate_selection([0, 2])

    # Selection returns a list of rows
    assert table.selection == [table.data[0], table.data[2]]

    # Selection handler was triggered
    on_select_handler.assert_called_once_with(table)


def test_activation(table, on_activate_handler):
    """A row can be activated."""

    # Activate an item
    table._impl.simulate_activate(1)

    # Activate handler was triggered; the activated row is provided
    on_activate_handler.assert_called_once_with(table, row=table.data[1])


def test_scroll_to_top(table):
    """A table can be scrolled to the top."""
    table.scroll_to_top()

    assert_action_performed_with(table, "scroll to row", row=0)


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
def test_scroll_to_row(table, row, effective):
    """A table can be scrolled to a specific row."""
    table.scroll_to_row(row)

    assert_action_performed_with(table, "scroll to row", row=effective)


def test_scroll_to_row_no_data(table):
    """If there's no data, scrolling is a no-op."""
    table.data.clear()

    table.scroll_to_row(5)

    assert_action_not_performed(table, "scroll to row")


def test_scroll_to_bottom(table):
    """A table can be scrolled to the top."""
    table.scroll_to_bottom()

    assert_action_performed_with(table, "scroll to row", row=2)


def test_insert_column_accessor(table):
    """A column can be inserted at an accessor."""
    table.insert_column("value", "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        heading="New Column",
        accessor="extra",
    )
    assert table.headings == ["Title", "New Column", "Value"]
    assert table.accessors == ["key", "extra", "value"]


def test_insert_column_unknown_accessor(table):
    """If the insertion index accessor is unknown, an error is raised."""
    with pytest.raises(ValueError, match=r"'unknown' is not in list"):
        table.insert_column("unknown", "New Column", accessor="extra")


def test_insert_column_index(table):
    """A column can be inserted."""

    table.insert_column(1, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        heading="New Column",
        accessor="extra",
    )
    assert table.headings == ["Title", "New Column", "Value"]
    assert table.accessors == ["key", "extra", "value"]


def test_insert_column_big_index(table):
    """A column can be inserted at an index bigger than the number of columns."""

    table.insert_column(100, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=2,
        heading="New Column",
        accessor="extra",
    )
    assert table.headings == ["Title", "Value", "New Column"]
    assert table.accessors == ["key", "value", "extra"]


def test_insert_column_negative_index(table):
    """A column can be inserted at a negative index."""

    table.insert_column(-2, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=0,
        heading="New Column",
        accessor="extra",
    )
    assert table.headings == ["New Column", "Title", "Value"]
    assert table.accessors == ["extra", "key", "value"]


def test_insert_column_big_negative_index(table):
    """A column can be inserted at a negative index larger than the number of
    columns."""

    table.insert_column(-100, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=0,
        heading="New Column",
        accessor="extra",
    )
    assert table.headings == ["New Column", "Title", "Value"]
    assert table.accessors == ["extra", "key", "value"]


def test_insert_column_no_accessor(table):
    """A column can be inserted with a default accessor."""

    table.insert_column(1, "New Column")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        heading="New Column",
        accessor="new_column",
    )
    assert table.headings == ["Title", "New Column", "Value"]
    assert table.accessors == ["key", "new_column", "value"]


def test_insert_column_no_headings(source):
    """A column can be inserted into a table with no headings."""
    table = toga.Table(headings=None, accessors=["key", "value"], data=source)

    table.insert_column(1, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        heading=None,
        accessor="extra",
    )
    assert table.headings is None
    assert table.accessors == ["key", "extra", "value"]


def test_insert_column_no_headings_missing_accessor(source):
    """An accessor is mandatory when adding a column to a table with no headings."""
    table = toga.Table(headings=None, accessors=["key", "value"], data=source)

    with pytest.raises(
        ValueError,
        match=r"Must specify an accessor on a table without headings",
    ):
        table.insert_column(1, "New Column")


def test_append_column(table):
    """A column can be appended."""
    table.append_column("New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=2,
        heading="New Column",
        accessor="extra",
    )
    assert table.headings == ["Title", "Value", "New Column"]
    assert table.accessors == ["key", "value", "extra"]


def test_remove_column_accessor(table):
    """A column can be removed by accessor."""

    table.remove_column("value")

    # The column was removed
    assert_action_performed_with(
        table,
        "remove column",
        index=1,
    )
    assert table.headings == ["Title"]
    assert table.accessors == ["key"]


def test_remove_column_unknown_accessor(table):
    """If the column named for removal doesn't exist, an error is raised."""
    with pytest.raises(ValueError, match=r"'unknown' is not in list"):
        table.remove_column("unknown")


def test_remove_column_invalid_index(table):
    """If the index specified doesn't exist, an error is raised."""
    with pytest.raises(IndexError, match=r"list assignment index out of range"):
        table.remove_column(100)


def test_remove_column_index(table):
    """A column can be removed by index."""

    table.remove_column(1)

    # The column was removed
    assert_action_performed_with(
        table,
        "remove column",
        index=1,
    )
    assert table.headings == ["Title"]
    assert table.accessors == ["key"]


def test_remove_column_negative_index(table):
    """A column can be removed by index."""

    table.remove_column(-2)

    # The column was removed
    assert_action_performed_with(
        table,
        "remove column",
        index=0,
    )
    assert table.headings == ["Value"]
    assert table.accessors == ["value"]


def test_remove_column_no_headings(table):
    """A column can be removed when there are no headings."""
    table = toga.Table(
        headings=None,
        accessors=["primus", "secondus"],
    )

    table.remove_column(1)

    # The column was removed
    assert_action_performed_with(
        table,
        "remove column",
        index=1,
    )
    assert table.headings is None
    assert table.accessors == ["primus"]


def test_deprecated_names(on_activate_handler):
    """Deprecated names still work."""

    # Can't specify both on_double_click and on_activate
    with pytest.raises(
        ValueError,
        match=r"Cannot specify both on_double_click and on_activate",
    ):
        toga.Table(["First", "Second"], on_double_click=Mock(), on_activate=Mock())

    # on_double_click is redirected at construction
    with pytest.warns(
        DeprecationWarning,
        match="Table.on_double_click has been renamed Table.on_activate",
    ):
        table = toga.Table(["First", "Second"], on_double_click=on_activate_handler)

    # on_double_click accessor is redirected to on_activate
    with pytest.warns(
        DeprecationWarning,
        match="Table.on_double_click has been renamed Table.on_activate",
    ):
        assert table.on_double_click._raw == on_activate_handler

    assert table.on_activate._raw == on_activate_handler

    # on_double_click mutator is redirected to on_activate
    new_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match="Table.on_double_click has been renamed Table.on_activate",
    ):
        table.on_double_click = new_handler

    assert table.on_activate._raw == new_handler

    # add_column redirects to insert
    table.add_column("New Column", "new_accessor")

    assert_action_performed_with(
        table,
        "insert column",
        index=2,
        heading="New Column",
        accessor="new_accessor",
    )
    assert table.headings == ["First", "Second", "New Column"]
    assert table.accessors == ["first", "second", "new_accessor"]
