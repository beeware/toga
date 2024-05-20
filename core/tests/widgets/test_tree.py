from unittest.mock import Mock

import pytest

import toga
from toga.sources import TreeSource
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
    source = TreeSource(
        data={
            ("group1", 1, "A**"): [
                (
                    {"key": "A first", "value": 110, "other": "AA*"},
                    None,
                ),
                (
                    {"key": "A second", "value": 120, "other": "AB*"},
                    [],
                ),
                (
                    {"key": "A third", "value": 130, "other": "AC*"},
                    [
                        ({"key": "A third-first", "value": 131, "other": "ACA"}, None),
                        ({"key": "A third-second", "value": 132, "other": "ACB"}, None),
                    ],
                ),
            ],
            ("group2", 2, "B**"): [
                (
                    {"key": "B first", "value": 210, "other": "BA*"},
                    None,
                ),
                (
                    {"key": "B second", "value": 220, "other": "BB*"},
                    [],
                ),
                (
                    {"key": "B third", "value": 230, "other": "BC*"},
                    [
                        ({"key": "B third-first", "value": 231, "other": "BCA"}, None),
                        ({"key": "B third-second", "value": 232, "other": "BCB"}, None),
                    ],
                ),
            ],
        },
        accessors=["key", "value"],
    )
    return source


@pytest.fixture
def tree(source, on_select_handler, on_activate_handler):
    return toga.Tree(
        ["Title", "Value"],
        accessors=["key", "value"],
        data=source,
        on_select=on_select_handler,
        on_activate=on_activate_handler,
    )


def test_tree_created():
    """A minimal Tree can be created."""
    tree = toga.Tree(["First", "Second"])
    assert tree._impl.interface is tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["First", "Second"]
    assert tree.accessors == ["first", "second"]
    assert not tree.multiple_select
    assert tree.missing_value == ""
    assert tree.on_select._raw is None
    assert tree.on_activate._raw is None


def test_create_with_values(source, on_select_handler, on_activate_handler):
    """A Tree can be created with initial values."""
    tree = toga.Tree(
        ["First", "Second"],
        data=source,
        accessors=["primus", "secondus"],
        multiple_select=True,
        on_select=on_select_handler,
        on_activate=on_activate_handler,
        missing_value="Boo!",
    )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 2
    assert tree.headings == ["First", "Second"]
    assert tree.accessors == ["primus", "secondus"]
    assert tree.multiple_select
    assert tree.missing_value == "Boo!"
    assert tree.on_select._raw == on_select_handler
    assert tree.on_activate._raw == on_activate_handler


def test_create_with_accessor_overrides():
    """A Tree can partially override accessors."""
    tree = toga.Tree(
        ["First", "Second"],
        accessors={"First": "override"},
    )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["First", "Second"]
    assert tree.accessors == ["override", "second"]


def test_create_no_headings():
    """A Tree can be created with no headings."""
    tree = toga.Tree(
        headings=None,
        accessors=["primus", "secondus"],
    )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings is None
    assert tree.accessors == ["primus", "secondus"]


def test_create_headings_required():
    """A Tree requires either headings can be created with no headings."""
    with pytest.raises(
        ValueError,
        match=r"Cannot create a tree without either headings or accessors",
    ):
        toga.Tree()


def test_disable_no_op(tree):
    """Tree doesn't have a disabled state."""
    # Enabled by default
    assert tree.enabled

    # Try to disable the widget
    tree.enabled = False

    # Still enabled.
    assert tree.enabled


def test_focus_noop(tree):
    """Focus is a no-op."""

    tree.focus()
    assert_action_not_performed(tree, "focus")


@pytest.mark.parametrize(
    "data, all_attributes, extra_attributes",
    [
        # Dictionary of single values
        (
            {
                "People": {
                    "Alice": None,
                    "Bob": None,
                    "Charlie": None,
                }
            },
            False,
            False,
        ),
        # Dictionary of tuples
        (
            {
                ("People", None, None): {
                    ("Alice", 123, "extra1"): None,
                    ("Bob", 234, "extra2"): None,
                    ("Charlie", 345, "extra4"): None,
                }
            },
            True,
            False,
        ),
        # List of tuples with tuples
        (
            [
                (
                    ("People", None, None),
                    [
                        (("Alice", 123, "extra1"), None),
                        (("Bob", 234, "extra2"), None),
                        (("Charlie", 345, "extra3"), None),
                    ],
                ),
            ],
            True,
            False,
        ),
        # List of tuples with Dictionaries
        (
            [
                (
                    {"key": "People"},
                    [
                        ({"key": "Alice", "value": 123, "other": "extra1"}, None),
                        ({"key": "Bob", "value": 234, "other": "extra2"}, None),
                        ({"key": "Charlie", "value": 345, "other": "extra3"}, None),
                    ],
                ),
            ],
            True,
            True,
        ),
    ],
)
def test_set_data(tree, on_select_handler, data, all_attributes, extra_attributes):
    """Data can be set from a variety of sources."""

    # The selection hasn't changed yet.
    on_select_handler.assert_not_called()

    # Change the data
    tree.data = data

    # This triggered the select handler
    on_select_handler.assert_called_once_with(tree)

    # A TreeSource has been constructed
    assert isinstance(tree.data, TreeSource)
    assert len(tree.data) == 1
    assert len(tree.data[0]) == 3

    # The accessors are mapped in order.
    assert tree.data[0].key == "People"

    assert tree.data[0][0].key == "Alice"
    assert tree.data[0][1].key == "Bob"
    assert tree.data[0][2].key == "Charlie"

    if all_attributes:
        assert tree.data[0][0].value == 123
        assert tree.data[0][1].value == 234
        assert tree.data[0][2].value == 345

    if extra_attributes:
        assert tree.data[0][0].other == "extra1"
        assert tree.data[0][1].other == "extra2"
        assert tree.data[0][2].other == "extra3"


def test_single_selection(tree, on_select_handler):
    """The current selection can be retrieved."""
    # Selection is initially empty
    assert tree.selection is None
    on_select_handler.assert_not_called()

    # Select an item
    tree._impl.simulate_selection((0, 1))

    # Selection returns a single row
    assert tree.selection == tree.data[0][1]

    # Selection handler was triggered
    on_select_handler.assert_called_once_with(tree)


def test_multiple_selection(source, on_select_handler):
    """A multi-select tree can have the selection retrieved."""
    tree = toga.Tree(
        ["Title", "Value"],
        data=source,
        multiple_select=True,
        on_select=on_select_handler,
    )
    # Selection is initially empty
    assert tree.selection == []
    on_select_handler.assert_not_called()

    # Select an item
    tree._impl.simulate_selection([(0, 1), (1, 2, 1)])

    # Selection returns a list of rows
    assert tree.selection == [tree.data[0][1], tree.data[1][2][1]]

    # Selection handler was triggered
    on_select_handler.assert_called_once_with(tree)


def test_expand_collapse(tree):
    """The rows on a tree can be expanded and collapsed."""

    # Expand the full tree
    tree.expand()
    assert_action_performed_with(tree, "expand all")

    # Collapse a single node
    tree.collapse(tree.data[1][2])
    assert_action_performed_with(tree, "collapse node", node=tree.data[1][2])

    # Expand a single node
    tree.expand(tree.data[1][2])
    assert_action_performed_with(tree, "expand node", node=tree.data[1][2])

    # Collapse a leaf node
    tree.collapse(tree.data[1][2][1])
    assert_action_performed_with(tree, "collapse node", node=tree.data[1][2][1])

    # Expand a leaf node
    tree.expand(tree.data[1][2][1])
    assert_action_performed_with(tree, "expand node", node=tree.data[1][2][1])

    # Collapse the full tree
    tree.collapse()
    assert_action_performed_with(tree, "collapse all")


def test_activation(tree, on_activate_handler):
    """A row can be activated."""

    # Activate an item
    tree._impl.simulate_activate((0, 1))

    # Activate handler was triggered; the activated node is provided
    on_activate_handler.assert_called_once_with(tree, node=tree.data[0][1])


def test_insert_column_accessor(tree):
    """A column can be inserted at an accessor."""
    tree.insert_column("value", "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        heading="New Column",
        accessor="extra",
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    assert tree.accessors == ["key", "extra", "value"]


def test_insert_column_unknown_accessor(tree):
    """If the insertion index accessor is unknown, an error is raised."""
    with pytest.raises(ValueError, match=r"'unknown' is not in list"):
        tree.insert_column("unknown", "New Column", accessor="extra")


def test_insert_column_index(tree):
    """A column can be inserted."""

    tree.insert_column(1, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        heading="New Column",
        accessor="extra",
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    assert tree.accessors == ["key", "extra", "value"]


def test_insert_column_big_index(tree):
    """A column can be inserted at an index bigger than the number of columns."""

    tree.insert_column(100, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=2,
        heading="New Column",
        accessor="extra",
    )
    assert tree.headings == ["Title", "Value", "New Column"]
    assert tree.accessors == ["key", "value", "extra"]


def test_insert_column_negative_index(tree):
    """A column can be inserted at a negative index."""

    tree.insert_column(-2, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=0,
        heading="New Column",
        accessor="extra",
    )
    assert tree.headings == ["New Column", "Title", "Value"]
    assert tree.accessors == ["extra", "key", "value"]


def test_insert_column_big_negative_index(tree):
    """A column can be inserted at a negative index larger than the number of
    columns."""

    tree.insert_column(-100, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=0,
        heading="New Column",
        accessor="extra",
    )
    assert tree.headings == ["New Column", "Title", "Value"]
    assert tree.accessors == ["extra", "key", "value"]


def test_insert_column_no_accessor(tree):
    """A column can be inserted with a default accessor."""

    tree.insert_column(1, "New Column")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        heading="New Column",
        accessor="new_column",
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    assert tree.accessors == ["key", "new_column", "value"]


def test_insert_column_no_headings(source):
    """A column can be inserted into a tree with no headings."""
    tree = toga.Tree(headings=None, accessors=["key", "value"], data=source)

    tree.insert_column(1, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        heading=None,
        accessor="extra",
    )
    assert tree.headings is None
    assert tree.accessors == ["key", "extra", "value"]


def test_insert_column_no_headings_missing_accessor(source):
    """An accessor is mandatory when adding a column to a tree with no headings."""
    tree = toga.Tree(headings=None, accessors=["key", "value"], data=source)

    with pytest.raises(
        ValueError,
        match=r"Must specify an accessor on a tree without headings",
    ):
        tree.insert_column(1, "New Column")


def test_append_column(tree):
    """A column can be appended."""
    tree.append_column("New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=2,
        heading="New Column",
        accessor="extra",
    )
    assert tree.headings == ["Title", "Value", "New Column"]
    assert tree.accessors == ["key", "value", "extra"]


def test_remove_column_accessor(tree):
    """A column can be removed by accessor."""

    tree.remove_column("value")

    # The column was removed
    assert_action_performed_with(
        tree,
        "remove column",
        index=1,
    )
    assert tree.headings == ["Title"]
    assert tree.accessors == ["key"]


def test_remove_column_unknown_accessor(tree):
    """If the column named for removal doesn't exist, an error is raised."""
    with pytest.raises(ValueError, match=r"'unknown' is not in list"):
        tree.remove_column("unknown")


def test_remove_column_invalid_index(tree):
    """If the index specified doesn't exist, an error is raised."""
    with pytest.raises(IndexError, match=r"list assignment index out of range"):
        tree.remove_column(100)


def test_remove_column_index(tree):
    """A column can be removed by index."""

    tree.remove_column(1)

    # The column was removed
    assert_action_performed_with(
        tree,
        "remove column",
        index=1,
    )
    assert tree.headings == ["Title"]
    assert tree.accessors == ["key"]


def test_remove_column_negative_index(tree):
    """A column can be removed by index."""

    tree.remove_column(-2)

    # The column was removed
    assert_action_performed_with(
        tree,
        "remove column",
        index=0,
    )
    assert tree.headings == ["Value"]
    assert tree.accessors == ["value"]


def test_remove_column_no_headings(tree):
    """A column can be removed when there are no headings."""
    tree = toga.Tree(
        headings=None,
        accessors=["primus", "secondus"],
    )

    tree.remove_column(1)

    # The column was removed
    assert_action_performed_with(
        tree,
        "remove column",
        index=1,
    )
    assert tree.headings is None
    assert tree.accessors == ["primus"]


def test_deprecated_names(on_activate_handler):
    """Deprecated names still work."""

    # Can't specify both on_double_click and on_activate
    with pytest.raises(
        ValueError,
        match=r"Cannot specify both on_double_click and on_activate",
    ):
        toga.Tree(["First", "Second"], on_double_click=Mock(), on_activate=Mock())

    # on_double_click is redirected at construction
    with pytest.warns(
        DeprecationWarning,
        match="Tree.on_double_click has been renamed Tree.on_activate",
    ):
        tree = toga.Tree(["First", "Second"], on_double_click=on_activate_handler)

    # on_double_click accessor is redirected to on_activate
    with pytest.warns(
        DeprecationWarning,
        match="Tree.on_double_click has been renamed Tree.on_activate",
    ):
        assert tree.on_double_click._raw == on_activate_handler

    assert tree.on_activate._raw == on_activate_handler

    # on_double_click mutator is redirected to on_activate
    new_handler = Mock()
    with pytest.warns(
        DeprecationWarning,
        match="Tree.on_double_click has been renamed Tree.on_activate",
    ):
        tree.on_double_click = new_handler

    assert tree.on_activate._raw == new_handler
