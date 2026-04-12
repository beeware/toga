from unittest.mock import Mock, patch

import pytest

import toga
from toga.sources import AccessorColumn, ListSource, Source
from toga_dummy.utils import (
    assert_action_not_performed,
    assert_action_performed,
    assert_action_performed_with,
)

ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE = (
    r"The `accessor` argument is deprecated. To specify a non-default "
    r"accessor for a column, use an `AccessorColumn`\. To specify the "
    r"ordering of accessors use a `ListSource` with an `accessors` "
    r"argument for the data\."
)

ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE = (
    r"The `accessors` argument is deprecated. To specify a non-default "
    r"accessor for a column, use an `AccessorColumn`\. To specify the "
    r"ordering of accessors use a `ListSource` with an `accessors` "
    r"argument for the data\."
)


class CustomRow:
    def __init__(self, key, value, extra):
        self.key = key
        self.value = value
        self.extra = extra


class ReadonlySource(Source):
    def __init__(self, data):
        super().__init__()
        self._data = list(data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


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
        [
            AccessorColumn("Title", "key"),
            AccessorColumn("Value", "value"),
        ],
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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["first", "second"]
    assert table.data.accessors == ["first", "second"]
    assert table.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]
    assert not table.multiple_select
    assert table.show_headings
    assert table.missing_value == ""
    assert table.on_select._raw is None
    assert table.on_activate._raw is None


def test_table_created_explicit_show_headings():
    """A minimal Table can be created with show headings True."""
    table = toga.Table(["First", "Second"], show_headings=True)
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["first", "second"]
    assert table.data.accessors == ["first", "second"]
    assert table.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]
    assert not table.multiple_select
    assert table.show_headings
    assert table.missing_value == ""
    assert table.on_select._raw is None
    assert table.on_activate._raw is None


def test_table_created_explicit_show_headings_false():
    """A minimal Table can be created with show headings False."""
    table = toga.Table(["First", "Second"], show_headings=False)
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings is None
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["first", "second"]
    assert table.data.accessors == ["first", "second"]
    assert table.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]
    assert not table.multiple_select
    assert not table.show_headings
    assert table.missing_value == ""
    assert table.on_select._raw is None
    assert table.on_activate._raw is None


def test_table_create_columns():
    """A Table can be created with column objects."""
    table = toga.Table(
        [
            AccessorColumn("First"),
            AccessorColumn("Second"),
        ]
    )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["first", "second"]
    assert table.data.accessors == ["first", "second"]
    assert table.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]


def test_table_create_columns_with_accessors():
    """A Table can be created with column objects that supply accessors."""
    table = toga.Table(
        [
            AccessorColumn("First", "primus"),
            AccessorColumn("Second", "secundus"),
        ]
    )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["primus", "secundus"]
    assert table.data.accessors == ["primus", "secundus"]
    assert table.columns == [
        AccessorColumn("First", "primus"),
        AccessorColumn("Second", "secundus"),
    ]


def test_create_with_values(source, on_select_handler, on_activate_handler):
    """A Table can be created with initial values."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table = toga.Table(
            ["First", "Second"],
            id="foobar",
            data=source,
            accessors=["primus", "secondus"],
            multiple_select=True,
            on_select=on_select_handler,
            on_activate=on_activate_handler,
            missing_value="Boo!",
            # A style property
            width=256,
        )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert table.id == "foobar"
    assert len(table.data) == 3
    assert table.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["primus", "secondus"]
    assert table.data.accessors == ["key", "value"]
    assert table.columns == [
        AccessorColumn("First", "primus"),
        AccessorColumn("Second", "secondus"),
    ]
    assert table.multiple_select
    assert table.missing_value == "Boo!"
    assert table.on_select._raw == on_select_handler
    assert table.on_activate._raw == on_activate_handler
    assert table.style.width == 256


def test_create_with_accessor_overrides():
    """A Table can partially override accessors."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table = toga.Table(
            ["First", "Second"],
            accessors={"First": "override"},
        )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["override", "second"]
    assert table.data.accessors == ["override", "second"]
    assert table.columns == [
        AccessorColumn("First", "override"),
        AccessorColumn("Second", "second"),
    ]


def test_create_headings():
    """A Table can be created with headings instead of columns."""
    with (
        pytest.warns(
            DeprecationWarning,
            match=(
                r"The 'headings' keyword argument is deprecated; use 'columns' instead."
            ),
        ),
        pytest.warns(
            DeprecationWarning,
            match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
        ),
    ):
        table = toga.Table(
            headings=["First", "Second"],
            accessors=["primus", "secondus"],
        )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["primus", "secondus"]
    assert table.data.accessors == ["primus", "secondus"]
    assert table.columns == [
        AccessorColumn("First", "primus"),
        AccessorColumn("Second", "secondus"),
    ]


def test_create_no_columns():
    """A Table can be created with no columns."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table = toga.Table(
            columns=None,
            accessors=["primus", "secondus"],
        )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings is None
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["primus", "secondus"]
    assert table.data.accessors == ["primus", "secondus"]
    assert table.columns == [
        AccessorColumn(None, "primus"),
        AccessorColumn(None, "secondus"),
    ]
    assert not table.show_headings


def test_create_no_columns_show_headings():
    """A Table can be created with no columns and show_headings True."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table = toga.Table(
            columns=None,
            accessors=["primus", "secondus"],
            show_headings=True,
        )
    assert table._impl.interface == table
    assert_action_performed(table, "create Table")

    assert len(table.data) == 0
    assert table.headings == ["", ""]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["primus", "secondus"]
    assert table.data.accessors == ["primus", "secondus"]
    assert table.columns == [
        AccessorColumn(None, "primus"),
        AccessorColumn(None, "secondus"),
    ]
    assert table.show_headings


def test_create_columns_required():
    """A Table requires either columns or accessors."""
    with pytest.raises(
        ValueError,
        match=r"Cannot create a table without either columns or accessors",
    ):
        toga.Table()


def test_create_columns_and_headings():
    """A Table cannot have both columns and headings."""
    with pytest.raises(
        TypeError,
        match=r"Can't specify columns and headings at the same time",
    ):
        toga.Table(columns=[], headings=[])


def test_disable_no_op(table):
    """Table doesn't have a disabled state."""
    # Enabled by default
    assert table.enabled

    # Try to disable the widget
    table.enabled = False

    # Still enabled.
    assert table.enabled


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
        # No data
        (
            None,
            False,
            False,
        ),
        # List source
        (
            ListSource(
                accessors=["key", "value"],
                data=[
                    {"key": "Alice", "value": 123, "extra": "extra1"},
                    {"key": "Bob", "value": 234, "extra": "extra2"},
                    {"key": "Charlie", "value": 345, "extra": "extra3"},
                ],
            ),
            True,
            True,
        ),
        # Custom read-only source
        (
            ReadonlySource(
                data=[
                    CustomRow("Alice", 123, "extra1"),
                    CustomRow("Bob", 234, "extra2"),
                    CustomRow("Charlie", 345, "extra3"),
                ]
            ),
            True,
            True,
        ),
    ],
)
def test_create_data(data, all_attributes, extra_attributes):
    """Data can be created from a variety of sources."""

    table = toga.Table(
        [
            AccessorColumn("Title", "key"),
            AccessorColumn("Value", "value"),
        ],
        data=data,
    )

    # The implementation is a listener on the new data
    assert table._impl in table.data.listeners

    if not isinstance(data, Source):
        # A ListSource has been constructed
        assert isinstance(table.data, ListSource)
    else:
        # The data is passed directly
        assert table.data is data
    if data is not None:
        assert len(table.data) == 3
    else:
        assert len(table.data) == 0

    # The table's accessors are what we expect
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value"]

    # The source's accessors are what we expect, if it has them
    if isinstance(table.data, ListSource):
        assert table.data.accessors == ["key", "value"]

    # The accessors are mapped in order.
    if data is not None:
        assert table.data[0].key == "Alice"
        assert table.data[2].key == "Charlie"

    if all_attributes:
        assert table.data[1].key == "Bob"
        assert table.data[0].value == 123
        assert table.data[1].value == 234
        assert table.data[2].value == 345
    elif data is not None:
        assert table.data[1].key == 1234

    if extra_attributes:
        assert table.data[0].extra == "extra1"
        assert table.data[1].extra == "extra2"
        assert table.data[2].extra == "extra3"


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
        # No data
        (
            None,
            False,
            False,
        ),
        # List source
        (
            ListSource(
                accessors=["key", "value"],
                data=[
                    {"key": "Alice", "value": 123, "extra": "extra1"},
                    {"key": "Bob", "value": 234, "extra": "extra2"},
                    {"key": "Charlie", "value": 345, "extra": "extra3"},
                ],
            ),
            True,
            True,
        ),
        # Custom read-only source
        (
            ReadonlySource(
                data=[
                    CustomRow("Alice", 123, "extra1"),
                    CustomRow("Bob", 234, "extra2"),
                    CustomRow("Charlie", 345, "extra3"),
                ]
            ),
            True,
            True,
        ),
    ],
)
def test_set_data(table, on_select_handler, data, all_attributes, extra_attributes):
    """Data can be set from a variety of sources."""

    # The selection hasn't changed yet.
    on_select_handler.assert_not_called()

    # The implementation is a listener on the data
    old_data = table.data
    assert table._impl in old_data.listeners

    # Change the data
    table.data = data

    # The implementation is not a listener on the old data
    assert table._impl not in old_data.listeners

    # The implementation is a listener on the new data
    assert table._impl in table.data.listeners

    # This triggered the select handler
    on_select_handler.assert_called_once_with(table)

    if not isinstance(data, Source):
        # A ListSource has been constructed
        assert isinstance(table.data, ListSource)
    else:
        # The data is passed directly
        assert table.data is data
    if data is not None:
        assert len(table.data) == 3
    else:
        assert len(table.data) == 0

    # The table's accessors are what we expect
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value"]

    # The source's accessors are what we expect, if it has them
    if isinstance(table.data, ListSource):
        assert table.data.accessors == ["key", "value"]

    # The accessors are mapped in order.
    if data is not None:
        assert table.data[0].key == "Alice"
        assert table.data[2].key == "Charlie"

    if all_attributes:
        assert table.data[1].key == "Bob"
        assert table.data[0].value == 123
        assert table.data[1].value == 234
        assert table.data[2].value == 345
    elif data is not None:
        assert table.data[1].key == 1234

    if extra_attributes:
        assert table.data[0].extra == "extra1"
        assert table.data[1].extra == "extra2"
        assert table.data[2].extra == "extra3"


def test_set_data_override_acessors(table, on_select_handler):
    """Setting data usually preserves accessors."""

    # The selection hasn't changed yet.
    on_select_handler.assert_not_called()

    # The implementation is a listener on the data
    old_data = table.data
    assert table._impl in old_data.listeners

    # Change the data
    table.data = ListSource(
        accessors=["key", "value", "extra"],
        data=[
            {"key": "Alice", "value": 123, "extra": "extra1"},
            {"key": "Bob", "value": 234, "extra": "extra2"},
            {"key": "Charlie", "value": 345, "extra": "extra3"},
        ],
    )

    # The implementation is not a listener on the old data
    assert table._impl not in old_data.listeners

    # The implementation is a listener on the new data
    assert table._impl in table.data.listeners

    # This triggered the select handler
    on_select_handler.assert_called_once_with(table)

    # The table's accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value"]

    # But the source's accessors have changed
    assert table.data.accessors == ["key", "value", "extra"]

    # Change the data to a list
    table.data = [
        {"key": "Alice", "value": 123, "extra": "extra1"},
        {"key": "Bob", "value": 234, "extra": "extra2"},
        {"key": "Charlie", "value": 345, "extra": "extra3"},
    ]

    # The accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value"]
    assert table.data.accessors == ["key", "value", "extra"]

    # Change the data to something without accessors
    table.data = ReadonlySource(
        data=[
            CustomRow("Alice", 123, "extra1"),
            CustomRow("Bob", 234, "extra2"),
            CustomRow("Charlie", 345, "extra3"),
        ]
    )

    # The table accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value"]

    # but the data doesn't have accessors
    assert not hasattr(table.data, "accessors")

    # Change the data back to a list
    table.data = [
        {"key": "Alice", "value": 123, "extra": "extra1"},
        {"key": "Bob", "value": 234, "extra": "extra2"},
        {"key": "Charlie", "value": 345, "extra": "extra3"},
    ]

    # The table's accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value"]

    # But the source's accessors have changed
    assert table.data.accessors == ["key", "value"]


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


def test_insert_column_object_by_index(table):
    """A column object can be inserted at a numerical index."""
    table.insert_column(1, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "extra", "value"]
    assert table.data.accessors == ["key", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_heading_by_accessor(table):
    """A column heading being inserted at an accessor is deprecated."""
    with pytest.warns(
        DeprecationWarning,
        match=(r"Using accessors is deprecated; use columns instead."),
    ):
        table.insert_column("value", AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "extra", "value"]
    assert table.data.accessors == ["key", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_unknown_accessor(table):
    """If the insertion index accessor is unknown, an error is raised."""
    with pytest.raises(ValueError, match=r"not in list"):
        with pytest.warns(
            DeprecationWarning,
            match=r"Using accessors is deprecated; use columns instead.",
        ):
            table.insert_column("unknown", AccessorColumn("New Column", "extra"))


def test_insert_column_heading_column_object_index(table):
    """A column can be inserted before another column object."""

    index_column = AccessorColumn("Value", "value")
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table.insert_column(index_column, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "extra", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_object_index_unknown_column(table):
    """If the insertion index accessor is unknown, an error is raised."""
    index_column = AccessorColumn("Unknown", "missing")
    with pytest.raises(ValueError, match=r"not in list"):
        table.insert_column(index_column, AccessorColumn("New Column", "extra"))


def test_insert_column_heading_by_index(table):
    """A column can be inserted."""

    with pytest.warns(
        DeprecationWarning,
        match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table.insert_column(1, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "extra", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_heading_by_index_heading_argument(table):
    """A column can be inserted with the deprecated heading argument."""
    with (
        pytest.warns(
            DeprecationWarning,
            match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
        ),
        pytest.warns(
            DeprecationWarning,
            match=(
                r"The 'heading' keyword argument is deprecated; use 'column' instead\."
            ),
        ),
    ):
        table.insert_column(1, heading="New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "extra", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_and_heading(table):
    """Can't use both column and heading arguments in insert_column."""

    with pytest.raises(
        TypeError,
        match=r"Can't specify both 'column' and 'heading' arguments\.",
    ):
        table.insert_column(1, AccessorColumn("New Column"), heading="New Column")


def test_insert_nothing(table):
    """Need either a column or an accessor when inserting."""

    with pytest.raises(
        ValueError,
        match=r"Must specify either a column or an accessor\.",
    ):
        table.insert_column(1)


def test_warn_accessor_ignored(table):
    """Accessor ignored when inserting a column object."""

    with (
        pytest.warns(
            DeprecationWarning,
            match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
        ),
        pytest.warns(
            UserWarning,
            match=(
                r"The 'accessor' argument is ignored when a column object is supplied\."
            ),
        ),
    ):
        table.insert_column(1, AccessorColumn("New Column"), accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "new_column"),
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "new_column", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "new_column"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_big_index(table):
    """A column can be inserted at an index bigger than the number of columns."""

    table.insert_column(100, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value", "extra"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_insert_column_negative_index(table):
    """A column can be inserted at a negative index."""

    table.insert_column(-2, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=0,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["New Column", "Title", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["extra", "key", "value"]
    assert table.columns == [
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_big_negative_index(table):
    """A column can be inserted at a negative index larger than the number of
    columns."""

    table.insert_column(-100, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=0,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["New Column", "Title", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["extra", "key", "value"]
    assert table.columns == [
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_no_accessor(table):
    """A column can be inserted with a default accessor."""

    table.insert_column(1, "New Column")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "new_column"),
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "new_column", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "new_column"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_no_headings(source):
    """A column can be inserted into a table with no headings."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table = toga.Table(columns=None, accessors=["key", "value"], data=source)

    table.insert_column(1, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings is None
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "extra", "value"]
    assert table.columns == [
        AccessorColumn(None, "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn(None, "value"),
    ]


def test_insert_column_no_headings_missing_accessor(source):
    """An accessor is mandatory when adding a column to a table with no headings."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table = toga.Table(columns=None, accessors=["key", "value"], data=source)

    with pytest.raises(
        ValueError,
        match=r"Must specify an accessor on a table without headings",
    ):
        table.insert_column(1, "New Column")


def test_insert_column_deprecated_implementation(table):
    """The old insert_column implementation API is deprecated."""

    def insert_column(self, index, heading, accessor):
        self._action("insert column", index=index, heading=heading, accessor=accessor)

    with patch.object(table._impl.__class__, "insert_column", insert_column):
        with pytest.warns(
            DeprecationWarning,
            match=(
                "Table implementations of insert_column should expect a column object "
                "not heading and accessor."
            ),
        ):
            table.insert_column(1, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=1,
        heading="New Column",
        accessor="extra",
    )
    assert table.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "extra", "value"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_append_column_object(table):
    """A column can be appended."""
    table.append_column(AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value", "extra"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_append_column_str(table):
    """A column can be appended using heading and accessor."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table.append_column("New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value", "extra"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_append_heading_deprecated(table):
    """Appending a column via heading keyword is deprecated."""
    with (
        pytest.warns(
            DeprecationWarning,
            match=(
                r"The 'heading' keyword argument is deprecated; use 'column' instead\."
            ),
        ),
        pytest.warns(
            DeprecationWarning,
            match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
        ),
    ):
        table.append_column(heading="New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        table,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert table.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key", "value", "extra"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_append_column_and_heading(table):
    """Can't use both column and heading arguments in append_column."""

    with pytest.raises(
        TypeError,
        match=r"Can't specify both 'column' and 'heading' arguments\.",
    ):
        table.append_column(AccessorColumn("New Column"), heading="New Column")


def test_remove_column_object(table):
    """A column can be removed by accessor."""

    table.remove_column(AccessorColumn("Value", "value"))

    # The column was removed
    assert_action_performed_with(
        table,
        "remove column",
        index=1,
    )
    assert table.headings == ["Title"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
    ]


def test_remove_column_accessor(table):
    """A column can be removed by accessor."""

    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        table.remove_column("value")

    # The column was removed
    assert_action_performed_with(
        table,
        "remove column",
        index=1,
    )
    assert table.headings == ["Title"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
    ]


def test_remove_column_unknown_accessor(table):
    """If the column named for removal doesn't exist, an error is raised."""

    with pytest.warns(
        DeprecationWarning,
        match=("Using accessors is deprecated; use columns instead."),
    ):
        with pytest.raises(ValueError, match=r"not in list"):
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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["key"]
    assert table.columns == [
        AccessorColumn("Title", "key"),
    ]


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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["value"]
    assert table.columns == [
        AccessorColumn("Value", "value"),
    ]


def test_remove_column_no_headings(table):
    """A column can be removed when there are no headings."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        table = toga.Table(
            columns=None,
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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert table.accessors == ["primus"]
    assert table.columns == [
        AccessorColumn(None, "primus"),
    ]
