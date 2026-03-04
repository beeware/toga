from unittest.mock import Mock, patch

import pytest

import toga
from toga.sources import AccessorColumn, Source, TreeSource
from toga_dummy.utils import (
    assert_action_performed,
    assert_action_performed_with,
)

ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE = (
    r"The `accessor` argument is deprecated. To specify a non-default "
    r"accessor for a column, use an `AccessorColumn`\. To specify the "
    r"ordering of accessors use a `TreeSource` with an `accessors` "
    r"argument for the data\."
)

ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE = (
    r"The `accessors` argument is deprecated. To specify a non-default "
    r"accessor for a column, use an `AccessorColumn`\. To specify the "
    r"ordering of accessors use a `TreeSource` with an `accessors` "
    r"argument for the data\."
)


class CustomNode:
    def __init__(self, key=None, value=None, other=None, children=None):
        self.key = key
        self.value = value
        self.other = other
        if children is not None:
            children = list(children)
        self._children = children

    def __len__(self):
        if self._children is not None:
            return len(self._children)

    def __getitem__(self, index):
        if self._children is not None:
            return self._children[index]
        else:
            raise IndexError("Node does not have children.")

    def can_have_children(self):
        return self._children is not None


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
        [
            AccessorColumn("Title", "key"),
            AccessorColumn("Value", "value"),
        ],
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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["first", "second"]
    assert tree.data.accessors == ["first", "second"]
    assert tree.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]
    assert not tree.multiple_select
    assert tree.show_headings
    assert tree.missing_value == ""
    assert tree.on_select._raw is None
    assert tree.on_activate._raw is None


def test_tree_created_explicit_show_headings():
    """A minimal Tree can be created with show headings True."""
    tree = toga.Tree(["First", "Second"], show_headings=True)
    assert tree._impl.interface is tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["first", "second"]
    assert tree.data.accessors == ["first", "second"]
    assert tree.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]
    assert not tree.multiple_select
    assert tree.show_headings
    assert tree.missing_value == ""
    assert tree.on_select._raw is None
    assert tree.on_activate._raw is None


def test_tree_created_explicit_show_headings_false():
    """A minimal Tree can be created with show headings False."""
    tree = toga.Tree(["First", "Second"], show_headings=False)
    assert tree._impl.interface is tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings is None
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["first", "second"]
    assert tree.data.accessors == ["first", "second"]
    assert tree.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]
    assert not tree.multiple_select
    assert not tree.show_headings
    assert tree.missing_value == ""
    assert tree.on_select._raw is None
    assert tree.on_activate._raw is None


def test_tree_create_columns():
    """A Tree can be created with column objects."""
    tree = toga.Tree(
        [
            AccessorColumn("First"),
            AccessorColumn("Second"),
        ]
    )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["first", "second"]
    assert tree.data.accessors == ["first", "second"]
    assert tree.columns == [
        AccessorColumn("First", "first"),
        AccessorColumn("Second", "second"),
    ]


def test_tree_create_columns_with_accessors():
    """A Tree can be created with column objects that supply accessors."""
    tree = toga.Tree(
        [
            AccessorColumn("First", "primus"),
            AccessorColumn("Second", "secundus"),
        ]
    )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["primus", "secundus"]
    assert tree.data.accessors == ["primus", "secundus"]
    assert tree.columns == [
        AccessorColumn("First", "primus"),
        AccessorColumn("Second", "secundus"),
    ]


def test_create_with_values(source, on_select_handler, on_activate_handler):
    """A Tree can be created with initial values."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree = toga.Tree(
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
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert tree.id == "foobar"
    assert len(tree.data) == 2
    assert tree.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["primus", "secondus"]
    assert tree.data.accessors == ["key", "value"]
    assert tree.multiple_select
    assert tree.missing_value == "Boo!"
    assert tree.on_select._raw == on_select_handler
    assert tree.on_activate._raw == on_activate_handler
    assert tree.style.width == 256


def test_create_with_accessor_overrides():
    """A Tree can partially override accessors."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree = toga.Tree(
            ["First", "Second"],
            accessors={"First": "override"},
        )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["override", "second"]
    assert tree.data.accessors == ["override", "second"]
    assert tree.columns == [
        AccessorColumn("First", "override"),
        AccessorColumn("Second", "second"),
    ]


def test_create_headings():
    """A Tree can be created with headings instead of columns."""
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
        tree = toga.Tree(
            headings=["First", "Second"],
            accessors=["primus", "secondus"],
        )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["First", "Second"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["primus", "secondus"]
    assert tree.data.accessors == ["primus", "secondus"]
    assert tree.columns == [
        AccessorColumn("First", "primus"),
        AccessorColumn("Second", "secondus"),
    ]


def test_create_no_columns():
    """A Tree can be created with no columns."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree = toga.Tree(
            headings=None,
            accessors=["primus", "secondus"],
        )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings is None
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["primus", "secondus"]
    assert tree.data.accessors == ["primus", "secondus"]
    assert tree.columns == [
        AccessorColumn(None, "primus"),
        AccessorColumn(None, "secondus"),
    ]
    assert not tree.show_headings


def test_create_no_columns_show_headings():
    """A Tree can be created with no columns and show_headings True."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree = toga.Tree(
            headings=None,
            accessors=["primus", "secondus"],
            show_headings=True,
        )
    assert tree._impl.interface == tree
    assert_action_performed(tree, "create Tree")

    assert len(tree.data) == 0
    assert tree.headings == ["", ""]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["primus", "secondus"]
    assert tree.data.accessors == ["primus", "secondus"]
    assert tree.columns == [
        AccessorColumn(None, "primus"),
        AccessorColumn(None, "secondus"),
    ]
    assert tree.show_headings


def test_create_columns_required():
    """A Tree requires either columns or accessors."""
    with pytest.raises(
        ValueError,
        match=r"Cannot create a tree without either columns or accessors",
    ):
        toga.Tree()


def test_create_columns_and_headings():
    """A Tree cannot have both columns and headings."""
    with pytest.raises(
        TypeError,
        match=r"Can't specify columns and headings at the same time",
    ):
        toga.Tree(columns=[], headings=[])


def test_disable_no_op(tree):
    """Tree doesn't have a disabled state."""
    # Enabled by default
    assert tree.enabled

    # Try to disable the widget
    tree.enabled = False

    # Still enabled.
    assert tree.enabled


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
        # No data
        (
            None,
            False,
            False,
        ),
        # Tree source
        (
            TreeSource(
                accessors=["key", "value"],
                data=[
                    (
                        {"key": "People"},
                        [
                            ({"key": "Alice", "value": 123, "other": "extra1"}, None),
                            ({"key": "Bob", "value": 234, "other": "extra2"}, None),
                            ({"key": "Charlie", "value": 345, "other": "extra3"}, None),
                        ],
                    ),
                ],
            ),
            True,
            True,
        ),
        # Custom read-only source
        (
            ReadonlySource(
                [
                    CustomNode(
                        "People",
                        children=[
                            CustomNode("Alice", 123, "extra1"),
                            CustomNode("Bob", 234, "extra2"),
                            CustomNode("Charlie", 345, "extra3"),
                        ],
                    )
                ]
            ),
            True,
            True,
        ),
    ],
)
def test_create_data(data, all_attributes, extra_attributes):
    """Data can be created from a variety of sources."""

    tree = toga.Tree(
        [
            AccessorColumn("Title", "key"),
            AccessorColumn("Value", "value"),
        ],
        data=data,
    )

    # The implementation is a listener on the data
    assert tree._impl in tree.data.listeners

    if not isinstance(data, Source):
        # A TreeSource has been constructed
        assert isinstance(tree.data, TreeSource)
    else:
        # data gets set directly
        assert tree.data is data

    # The tree's accessors are what we expect
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value"]

    # The source's accessors are what we expect, if it has them
    if isinstance(tree.data, TreeSource):
        assert tree.data.accessors == ["key", "value"]

    if data is None:
        assert len(tree.data) == 0
    else:
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
        # No data
        (
            None,
            False,
            False,
        ),
        # Tree source
        (
            TreeSource(
                accessors=["key", "value"],
                data=[
                    (
                        {"key": "People"},
                        [
                            ({"key": "Alice", "value": 123, "other": "extra1"}, None),
                            ({"key": "Bob", "value": 234, "other": "extra2"}, None),
                            ({"key": "Charlie", "value": 345, "other": "extra3"}, None),
                        ],
                    ),
                ],
            ),
            True,
            True,
        ),
        # Custom read-only source
        (
            ReadonlySource(
                [
                    CustomNode(
                        "People",
                        children=[
                            CustomNode("Alice", 123, "extra1"),
                            CustomNode("Bob", 234, "extra2"),
                            CustomNode("Charlie", 345, "extra3"),
                        ],
                    )
                ]
            ),
            True,
            True,
        ),
    ],
)
def test_set_data(tree, on_select_handler, data, all_attributes, extra_attributes):
    """Data can be set from a variety of sources."""

    # The selection hasn't changed yet.
    on_select_handler.assert_not_called()

    # The implementation is a listener on the data
    old_data = tree.data
    assert tree._impl in old_data.listeners

    # Change the data
    tree.data = data

    # The implementation is not a listener on the old data
    assert tree._impl not in old_data.listeners

    # The implementation is a listener on the data
    assert tree._impl in tree.data.listeners

    # This triggered the select handler
    on_select_handler.assert_called_once_with(tree)

    if not isinstance(data, Source):
        # A TreeSource has been constructed
        assert isinstance(tree.data, TreeSource)
    else:
        # data gets set directly
        assert tree.data is data

    # The tree's accessors are what we expect
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value"]

    # The source's accessors are what we expect, if it has them
    if isinstance(tree.data, TreeSource):
        assert tree.data.accessors == ["key", "value"]

    if data is None:
        assert len(tree.data) == 0
    else:
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


def test_set_data_override_acessors(tree, on_select_handler):
    """Setting data usually preserves accessors."""

    # The selection hasn't changed yet.
    on_select_handler.assert_not_called()

    # The implementation is a listener on the data
    old_data = tree.data
    assert tree._impl in old_data.listeners

    # Change the data
    tree.data = TreeSource(
        accessors=["key", "value", "extra"],
        data={
            ("People", None, None): {
                ("Alice", 123, "extra1"): None,
                ("Bob", 234, "extra2"): None,
                ("Charlie", 345, "extra4"): None,
            }
        },
    )

    # The implementation is not a listener on the old data
    assert tree._impl not in old_data.listeners

    # The implementation is a listener on the new data
    assert tree._impl in tree.data.listeners

    # This triggered the select handler
    on_select_handler.assert_called_once_with(tree)

    # The tree's accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value"]

    # But the source's accessors have changed
    assert tree.data.accessors == ["key", "value", "extra"]

    # Change the data to a list
    tree.data = [
        (
            ("People", None, None),
            [
                (("Alice", 123, "extra1"), None),
                (("Bob", 234, "extra2"), None),
                (("Charlie", 345, "extra3"), None),
            ],
        ),
    ]

    # The accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value"]
    assert tree.data.accessors == ["key", "value", "extra"]

    # Change the data to something without accessors
    tree.data = ReadonlySource(
        [
            CustomNode(
                "People",
                children=[
                    CustomNode("Alice", 123, "extra1"),
                    CustomNode("Bob", 234, "extra2"),
                    CustomNode("Charlie", 345, "extra3"),
                ],
            )
        ]
    )

    # The tree accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value"]

    # but the data doesn't have accessors
    assert not hasattr(tree.data, "accessors")

    # Change the data back to a list
    tree.data = [
        (
            ("People", None, None),
            [
                (("Alice", 123, "extra1"), None),
                (("Bob", 234, "extra2"), None),
                (("Charlie", 345, "extra3"), None),
            ],
        ),
    ]

    # The tree's accessors have not changed
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value"]

    # But the source's accessors have changed
    assert tree.data.accessors == ["key", "value"]


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


def test_insert_column_object_by_index(tree):
    """A column object can be inserted at a numerical index."""
    tree.insert_column(1, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "extra", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_heading_by_accessor(tree):
    """A column heading being inserted at an accessor is deprecated."""
    with (
        pytest.warns(
            DeprecationWarning,
            match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
        ),
        pytest.warns(
            DeprecationWarning,
            match=r"Using accessors is deprecated; use columns instead.",
        ),
    ):
        tree.insert_column("value", "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "extra", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_unknown_accessor(tree):
    """If the insertion index accessor is unknown, an error is raised."""
    with (
        pytest.warns(
            DeprecationWarning,
            match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
        ),
        pytest.warns(
            DeprecationWarning,
            match=r"Using accessors is deprecated; use columns instead.",
        ),
    ):
        with pytest.raises(ValueError, match=r"not in list"):
            tree.insert_column("unknown", "New Column", accessor="extra")


def test_insert_column_heading_column_object_index(tree):
    """A column can be inserted before another column object."""

    index_column = AccessorColumn("Value", "value")
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree.insert_column(index_column, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "extra", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_object_index_unknown_column(tree):
    """If the insertion index accessor is unknown, an error is raised."""
    index_column = AccessorColumn("Unknown", "missing")
    with pytest.raises(ValueError, match=r"not in list"):
        tree.insert_column(index_column, AccessorColumn("New Column", "extra"))


def test_insert_column_heading_by_index(tree):
    """A column can be inserted."""

    with pytest.warns(
        DeprecationWarning,
        match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree.insert_column(1, "New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "extra", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_heading_by_index_heading_argument(tree):
    """A column can be inserted with the deprecated heading argument."""

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
        tree.insert_column(1, heading="New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "extra", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_and_heading(tree):
    """Can't use both column and heading arguments in insert_column."""

    with pytest.raises(
        TypeError,
        match=r"Can't specify both 'column' and 'heading' arguments\.",
    ):
        tree.insert_column(1, AccessorColumn("New Column"), heading="New Column")


def test_insert_nothing(tree):
    """Need either a column or an accessor when inserting."""

    with pytest.raises(
        ValueError,
        match=r"Must specify either a column or an accessor\.",
    ):
        tree.insert_column(1)


def test_warn_accessor_ignored(tree):
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
        tree.insert_column(1, AccessorColumn("New Column"), accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "new_column"),
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "new_column", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "new_column"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_big_index(tree):
    """A column can be inserted at an index bigger than the number of columns."""

    tree.insert_column(100, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value", "extra"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_insert_column_negative_index(tree):
    """A column can be inserted at a negative index."""

    tree.insert_column(-2, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=0,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["New Column", "Title", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["extra", "key", "value"]
    assert tree.columns == [
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_big_negative_index(tree):
    """A column can be inserted at a negative index larger than the number of
    columns."""

    tree.insert_column(-100, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=0,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["New Column", "Title", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["extra", "key", "value"]
    assert tree.columns == [
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_no_accessor(tree):
    """A column can be inserted with a default accessor."""

    tree.insert_column(1, "New Column")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "new_column"),
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "new_column", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "new_column"),
        AccessorColumn("Value", "value"),
    ]


def test_insert_column_no_headings(source):
    """A column can be inserted into a tree with no headings."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree = toga.Tree(columns=None, accessors=["key", "value"], data=source)

    tree.insert_column(1, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings is None
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "extra", "value"]
    assert tree.columns == [
        AccessorColumn(None, "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn(None, "value"),
    ]


def test_insert_column_no_headings_missing_accessor(source):
    """An accessor is mandatory when adding a column to a tree with no headings."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree = toga.Tree(headings=None, accessors=["key", "value"], data=source)

    with pytest.raises(
        ValueError,
        match=r"Must specify an accessor on a tree without headings",
    ):
        tree.insert_column(1, "New Column")


def test_insert_column_deprecated_implementation(tree):
    """The old insert_column implementation API is deprecated."""

    def insert_column(self, index, heading, accessor):
        self._action("insert column", index=index, heading=heading, accessor=accessor)

    with patch.object(tree._impl.__class__, "insert_column", insert_column):
        with pytest.warns(
            DeprecationWarning,
            match=(
                "Tree implementations of insert_column should expect a column object "
                "not heading and accessor."
            ),
        ):
            tree.insert_column(1, AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=1,
        heading="New Column",
        accessor="extra",
    )
    assert tree.headings == ["Title", "New Column", "Value"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "extra", "value"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("New Column", "extra"),
        AccessorColumn("Value", "value"),
    ]


def test_append_column_object(tree):
    """A column can be appended."""
    tree.append_column(AccessorColumn("New Column", "extra"))

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value", "extra"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_append_column_str(tree):
    """A column can be appended using heading and accessor."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSOR_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree.append_column("New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value", "extra"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_append_heading_deprecated(tree):
    """Appending a column via heading keyword is deprecated."""
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
        tree.append_column(heading="New Column", accessor="extra")

    # The column was added
    assert_action_performed_with(
        tree,
        "insert column",
        index=2,
        column=AccessorColumn("New Column", "extra"),
    )
    assert tree.headings == ["Title", "Value", "New Column"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key", "value", "extra"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
        AccessorColumn("Value", "value"),
        AccessorColumn("New Column", "extra"),
    ]


def test_append_column_and_heading(tree):
    """Can't use both column and heading arguments in append_column."""

    with pytest.raises(
        TypeError,
        match=r"Can't specify both 'column' and 'heading' arguments\.",
    ):
        tree.append_column(AccessorColumn("New Column"), heading="New Column")


def test_remove_column_object(tree):
    """A column can be removed by accessor."""

    tree.remove_column(AccessorColumn("Value", "value"))

    # The column was removed
    assert_action_performed_with(
        tree,
        "remove column",
        index=1,
    )
    assert tree.headings == ["Title"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
    ]


def test_remove_column_accessor(tree):
    """A column can be removed by accessor."""

    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        tree.remove_column("value")

    # The column was removed
    assert_action_performed_with(
        tree,
        "remove column",
        index=1,
    )
    assert tree.headings == ["Title"]
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
    ]


def test_remove_column_unknown_accessor(tree):
    """If the column named for removal doesn't exist, an error is raised."""

    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        with pytest.raises(ValueError, match=r"not in list"):
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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["key"]
    assert tree.columns == [
        AccessorColumn("Title", "key"),
    ]


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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["value"]
    assert tree.columns == [
        AccessorColumn("Value", "value"),
    ]


def test_remove_column_no_headings(tree):
    """A column can be removed when there are no headings."""
    with pytest.warns(
        DeprecationWarning,
        match=ACCESSORS_OVERRIDES_EXCEPTION_MESSAGE,
    ):
        tree = toga.Tree(
            columns=None,
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
    with pytest.warns(
        DeprecationWarning,
        match=r"Using accessors is deprecated; use columns instead.",
    ):
        assert tree.accessors == ["primus"]
    assert tree.columns == [
        AccessorColumn(None, "primus"),
    ]
