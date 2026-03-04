import pytest

from toga.icons import Icon
from toga.sources import AccessorColumn, Column
from toga.sources.list_source import Row
from toga.widgets.label import Label


class ValueWithIcon:
    def __init__(self, icon, text):
        self.icon = icon
        self.text = text

    def __str__(self):
        return str(self.text)

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.text == other.text
            and self.icon == other.icon
        )


class ValueWithoutIcon:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return str(self.text)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.text == other.text


class SimpleColumn(Column):
    def value(self, row):
        return row


LABEL_WIDGET = Label("Test")


@pytest.mark.parametrize(
    "heading, heading_property",
    [
        ("Heading", "Heading"),
        (None, ""),
    ],
)
def test_column_abc(heading, heading_property):
    dummy_row = object()
    column = Column(heading)

    assert column.heading == heading_property
    assert column.value(dummy_row) is None
    assert column.text(dummy_row) is None
    assert column.text(dummy_row, "default") == "default"
    assert column.icon(dummy_row) is None
    assert column.widget(dummy_row) is None


def test_column_subclass():
    dummy_row = ("row",)
    column = SimpleColumn("test")

    assert column.heading == "test"
    assert column.value(dummy_row) == ("row",)
    assert column.text(dummy_row) == "('row',)"
    assert column.text(dummy_row, "default") == "('row',)"
    assert column.icon(dummy_row) is None
    assert column.widget(dummy_row) is None


@pytest.mark.parametrize(
    "heading, accessor, heading_property, accessor_property",
    [
        ("Heading", "name", "Heading", "name"),
        (None, "name", "", "name"),
        ("Heading", None, "Heading", "heading"),
    ],
)
def test_accessor_column(heading, accessor, heading_property, accessor_property):
    """An AccessorColumn can be created with a heading, and accessor, or both."""
    column = AccessorColumn(heading, accessor)

    assert column.heading == heading_property
    assert column.accessor == accessor_property


def test_accessor_column_equality():
    """AccessorColumns can be compared for equality."""
    column = AccessorColumn("title", "attribute")

    assert column == AccessorColumn("title", "attribute")
    assert column != AccessorColumn("title")
    assert column != AccessorColumn(accessor="attribute")
    assert column != Column("test")


def test_accessor_column_repr():
    """AccessorColumn have a repr()."""
    column = AccessorColumn("title", "attribute")

    assert repr(column) == "AccessorColumn(heading='title', accessor='attribute')"


def test_accessor_column_hash():
    """AccessorColumns can be hashed."""
    column = AccessorColumn("title", "attribute")

    assert hash(column) == hash((AccessorColumn, "title", "attribute"))


def test_accessor_column_failure():
    """An AccessorColumn requires at least an heading or an accessor."""
    with pytest.raises(
        ValueError,
        match="Cannot create a column without either headings or accessors",
    ):
        AccessorColumn(None, None)


@pytest.mark.parametrize(
    "headings, overrides, accessors",
    [
        # No overrides
        (
            ["First Col", "Second Col", "Third Col"],
            None,
            ["first_col", "second_col", "third_col"],
        ),
        # Explicitly provided accessors
        (
            ["First Col", "Second Col", "Third Col"],
            ["first", "second", "third"],
            ["first", "second", "third"],
        ),
        # Override some accessors
        (
            ["First Col", "Second Col", "Third Col"],
            ["first", "second", None],
            ["first", "second", "third_col"],
        ),
        # Override some accessors using dictionary
        (
            ["First Col", "Second Col", "Third Col"],
            {"First Col": "first", "Second Col": "second"},
            ["first", "second", "third_col"],
        ),
    ],
)
def test_columns_from_headings_and_accessors(headings, overrides, accessors):
    """Columns can be constructed with accessors derived from headings."""
    columns = AccessorColumn.columns_from_headings_and_accessors(headings, overrides)

    assert [column.heading for column in columns] == headings
    assert [column.accessor for column in columns] == accessors


def test_columns_from_headings_and_accessors_headings_none():
    """Columns can be constructed without headings."""
    accessors = ["first", "second", "third"]
    columns = AccessorColumn.columns_from_headings_and_accessors(None, accessors)

    assert [column.heading for column in columns] == ["", "", ""]
    assert [column.accessor for column in columns] == accessors


def test_columns_from_headings_and_accessors_failure():
    """Columns construction must provide headings or accessors."""
    with pytest.raises(
        ValueError,
        match="Cannot create columns without either headings or accessors.",
    ):
        AccessorColumn.columns_from_headings_and_accessors(None, None)


@pytest.mark.parametrize(
    "row, value, text, icon, widget",
    [
        (Row(), None, None, None, None),
        (Row(y=1), None, None, None, None),
        (Row(x=1), 1, "1", None, None),
        (Row(x="test"), "test", "test", None, None),
        (Row(x=(None, "test")), (None, "test"), "test", None, None),
        (Row(x=(None, 1)), (None, 1), "1", None, None),
        (Row(x=(None, None)), (None, None), None, None, None),
        (
            Row(x=(Icon.DEFAULT_ICON, "test")),
            (Icon.DEFAULT_ICON, "test"),
            "test",
            Icon.DEFAULT_ICON,
            None,
        ),
        (
            Row(x=(Icon.DEFAULT_ICON, 1)),
            (Icon.DEFAULT_ICON, 1),
            "1",
            Icon.DEFAULT_ICON,
            None,
        ),
        (
            Row(x=(Icon.DEFAULT_ICON, None)),
            (Icon.DEFAULT_ICON, None),
            None,
            Icon.DEFAULT_ICON,
            None,
        ),
        (
            Row(x=ValueWithIcon(Icon.DEFAULT_ICON, "test")),
            ValueWithIcon(Icon.DEFAULT_ICON, "test"),
            "test",
            Icon.DEFAULT_ICON,
            None,
        ),
        (
            Row(x=ValueWithIcon(Icon.DEFAULT_ICON, 1)),
            ValueWithIcon(Icon.DEFAULT_ICON, 1),
            "1",
            Icon.DEFAULT_ICON,
            None,
        ),
        (
            Row(x=ValueWithoutIcon("test")),
            ValueWithoutIcon("test"),
            "test",
            None,
            None,
        ),
        (
            Row(x=ValueWithoutIcon(1)),
            ValueWithoutIcon(1),
            "1",
            None,
            None,
        ),
        (
            Row(x=LABEL_WIDGET),
            LABEL_WIDGET,
            None,
            None,
            LABEL_WIDGET,
        ),
        # Issue #4135: List of 2 items is just data
        (Row(x=[None, "test"]), [None, "test"], "[None, 'test']", None, None),
        # Issue #4135: Tuple of 1 item is undefined; raise an error
        (Row(x=("test",)), ("test",), ValueError, ValueError, None),
        # Issue #4135: Tuple of 3+ items is undefined; raise an error
        (
            Row(x=(None, "test", 42)),
            (None, "test", 42),
            ValueError,
            ValueError,
            None,
        ),
    ],
)
def test_accessor_column_values(row, value, text, icon, widget):
    """Values can be accessed from a row using a column."""
    column = AccessorColumn(None, "x")

    assert column.value(row) == value
    assert column.widget(row) == widget

    if text is ValueError:
        with pytest.raises(ValueError, match=r"Data tuples must have length 2"):
            column.text(row)

        with pytest.raises(ValueError, match=r"Data tuples must have length 2"):
            column.icon(row)

    else:
        assert column.text(row) == text
        assert column.icon(row) == icon


DEFAULT = "default"


@pytest.mark.parametrize(
    "row, text",
    [
        (Row(), DEFAULT),
        (Row(y=1), DEFAULT),
        (Row(x=1), "1"),
        (Row(x="test"), "test"),
        (Row(x=(None, "test")), "test"),
        (Row(x=(None, 1)), "1"),
        (Row(x=(None, None)), DEFAULT),
        (
            Row(x=(Icon.DEFAULT_ICON, "test")),
            "test",
        ),
        (
            Row(x=(Icon.DEFAULT_ICON, 1)),
            "1",
        ),
        (
            Row(x=(Icon.DEFAULT_ICON, None)),
            DEFAULT,
        ),
        (
            Row(x=ValueWithIcon(Icon.DEFAULT_ICON, "test")),
            "test",
        ),
        (
            Row(x=ValueWithIcon(Icon.DEFAULT_ICON, 1)),
            "1",
        ),
        (
            Row(x=ValueWithoutIcon("test")),
            "test",
        ),
        (
            Row(x=ValueWithoutIcon(1)),
            "1",
        ),
        (
            Row(x=LABEL_WIDGET),
            DEFAULT,
        ),
    ],
)
def test_accessor_column_text_default(row, text):
    """Columns fall back to a default value when required."""
    column = AccessorColumn(None, "x")

    assert column.text(row, DEFAULT) == text
