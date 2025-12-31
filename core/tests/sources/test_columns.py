import pytest

from toga.sources.accessors import to_accessor
from toga.sources.columns import AccessorColumn


@pytest.mark.parametrize(
    "heading, accessor", [("Heading", "name"), (None, "name"), ("Heading", None)]
)
def test_accessor_column(heading, accessor):
    column = AccessorColumn(heading, accessor)

    assert column.heading == heading
    assert column.accessor == (
        accessor if accessor is not None else to_accessor(heading)
    )


def test_accessor_column_failure():
    with pytest.raises(
        ValueError, match="Cannot create a column without either headings or accessors"
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
    columns = AccessorColumn.columns_from_headings_and_accessors(headings, overrides)

    assert [column.heading for column in columns] == headings
    assert [column.accessor for column in columns] == accessors


def test_columns_from_headings_and_accessors_headings_none():
    accessors = ["first", "second", "third"]
    columns = AccessorColumn.columns_from_headings_and_accessors(None, accessors)

    assert [column.heading for column in columns] == [None, None, None]
    assert [column.accessor for column in columns] == accessors


def test_columns_from_headings_and_accessors_failure():
    with pytest.raises(
        ValueError, match="Cannot create columns without either headings or accessors."
    ):
        AccessorColumn.columns_from_headings_and_accessors(None, None)
