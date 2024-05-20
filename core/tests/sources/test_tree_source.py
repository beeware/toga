from unittest.mock import Mock

import pytest

from toga.sources import Node, TreeSource


@pytest.fixture
def listener():
    return Mock()


@pytest.fixture
def source(listener):
    source = TreeSource(
        data={
            ("group1", 1): [
                (
                    {"val1": "A first", "val2": 110},
                    None,
                ),
                (
                    {"val1": "A second", "val2": 120},
                    [],
                ),
                (
                    {"val1": "A third", "val2": 130},
                    [
                        ({"val1": "A third-first", "val2": 131}, None),
                        ({"val1": "A third-second", "val2": 132}, None),
                    ],
                ),
            ],
            ("group2", 2): [
                (
                    {"val1": "B first", "val2": 210},
                    None,
                ),
                (
                    {"val1": "B second", "val2": 220},
                    [],
                ),
                (
                    {"val1": "B third", "val2": 230},
                    [
                        ({"val1": "B third-first", "val2": 231}, None),
                        ({"val1": "B third-second", "val2": 232}, None),
                    ],
                ),
            ],
        },
        accessors=["val1", "val2"],
    )

    source.add_listener(listener)
    return source


@pytest.mark.parametrize(
    "value",
    [
        None,
        42,
        "not a list",
    ],
)
def test_invalid_accessors(value):
    """Accessors for a list source must be a list of attribute names."""
    with pytest.raises(
        ValueError,
        match=r"accessors should be a list of attribute names",
    ):
        TreeSource(accessors=value)


def test_accessors_required():
    """A list source must specify *some* accessors."""
    with pytest.raises(
        ValueError,
        match=r"TreeSource must be provided a list of accessors",
    ):
        TreeSource(accessors=[], data=[1, 2, 3])


def test_accessors_copied():
    """A list source must specify *some* accessors."""
    accessors = ["foo", "bar"]
    source = TreeSource(accessors)

    assert source._accessors == ["foo", "bar"]

    # The accessors have been copied.
    accessors.append("whiz")
    assert source._accessors == ["foo", "bar"]


@pytest.mark.parametrize(
    "data",
    [
        {},
        [],
    ],
)
def test_create_empty(data):
    """An empty TreeSource can be created."""
    source = TreeSource(data=data, accessors=["val1", "val2"])

    assert len(source) == 0


@pytest.mark.parametrize(
    "data, all_accessor_levels",
    [
        # Dictionaries all the way down
        (
            {
                "root0": {
                    "child00": None,
                    "child01": {},
                    "child02": {"child020": None, "child021": None},
                },
                "root1": {
                    "child10": None,
                    "child11": {},
                    "child12": {"child120": None, "child121": None},
                },
            },
            set(),  # Only the first accessor is ever used
        ),
        # Dictionaries with tuples as keys
        (
            {
                ("root0", 1): {
                    ("child00", 11): None,
                    ("child01", 12): {},
                    ("child02", 13): {("child020", 131): None, ("child021", 132): None},
                },
                ("root1", 2): {
                    ("child10", 21): None,
                    ("child11", 22): {},
                    ("child12", 23): {("child120", 231): None, ("child121", 232): None},
                },
            },
            {0, 1, 2},  # All accessors at all levels
        ),
        # List of dictionary data, list children
        (
            [
                (
                    {"val1": "root0", "val2": 1},
                    [
                        ({"val1": "child00", "val2": 11}, None),
                        ({"val1": "child01", "val2": 12}, []),
                        (
                            {"val1": "child02", "val2": 13},
                            [
                                ({"val1": "child020", "val2": 131}, None),
                                ({"val1": "child021", "val2": 132}, None),
                            ],
                        ),
                    ],
                ),
                (
                    {"val1": "root1", "val2": 2},
                    [
                        ({"val1": "child10", "val2": 21}, None),
                        ({"val1": "child11", "val2": 22}, []),
                        (
                            {"val1": "child12", "val2": 23},
                            [
                                ({"val1": "child120", "val2": 231}, None),
                                ({"val1": "child121", "val2": 232}, None),
                            ],
                        ),
                    ],
                ),
            ],
            {0, 1, 2},  # all accessors at all levels.
        ),
        # List of tuple data, list children
        (
            [
                (
                    ("root0", 1),
                    [
                        (("child00", 11), None),
                        (("child01", 12), []),
                        (
                            ("child02", 13),
                            [
                                (("child020", 131), None),
                                (("child021", 132), None),
                            ],
                        ),
                    ],
                ),
                (
                    ("root1", 2),
                    [
                        (("child10", 21), None),
                        (("child11", 22), []),
                        (
                            ("child12", 23),
                            [
                                (("child120", 231), None),
                                (("child121", 232), None),
                            ],
                        ),
                    ],
                ),
            ],
            {0, 1, 2},  # all accessors at all levels.
        ),
        # Dictionary of lists of dictionary data, list children
        (
            {
                "root0": [
                    ({"val1": "child00", "val2": 11}, None),
                    ({"val1": "child01", "val2": 12}, []),
                    (
                        {"val1": "child02", "val2": 13},
                        [
                            ({"val1": "child020", "val2": 131}, None),
                            ({"val1": "child021", "val2": 132}, None),
                        ],
                    ),
                ],
                "root1": [
                    ({"val1": "child10", "val2": 21}, None),
                    ({"val1": "child11", "val2": 22}, []),
                    (
                        {"val1": "child12", "val2": 23},
                        [
                            ({"val1": "child120", "val2": 231}, None),
                            ({"val1": "child121", "val2": 232}, None),
                        ],
                    ),
                ],
            },
            {1, 2},  # Accessors everywhere except the root.
        ),
        # List of dictionary data, dictionary children at level 1
        (
            [
                (
                    {"val1": "root0", "val2": 1},
                    {
                        "child00": None,
                        "child01": {},
                        "child02": [
                            ({"val1": "child020", "val2": 131}, None),
                            ({"val1": "child021", "val2": 132}, None),
                        ],
                    },
                ),
                (
                    {"val1": "root1", "val2": 2},
                    {
                        "child10": None,
                        "child11": {},
                        "child12": [
                            ({"val1": "child120", "val2": 231}, None),
                            ({"val1": "child121", "val2": 232}, None),
                        ],
                    },
                ),
            ],
            {0, 2},  # all accessors at first and last level
        ),
    ],
)
def test_create(data, all_accessor_levels):
    """A tree source can be created from data in different formats."""
    source = TreeSource(data=data, accessors=["val1", "val2"])

    # Source has 2 roots
    assert len(source) == 2

    # Root0 has 2 children
    assert source[0].val1 == "root0"
    assert len(source[0]) == 3
    assert source[0].can_have_children()

    # Root1 has 2 children
    assert source[1].val1 == "root1"
    assert len(source[1]) == 3
    assert source[1].can_have_children()

    # If level 0 has all accessors, check them as well.
    if 0 in all_accessor_levels:
        assert source[0].val2 == 1
        assert source[1].val2 == 2

    # Children of root 0
    assert source[0][0].val1 == "child00"
    assert len(source[0][0]) == 0
    assert not source[0][0].can_have_children()

    assert source[0][1].val1 == "child01"
    assert len(source[0][1]) == 0
    assert source[0][1].can_have_children()

    assert source[0][2].val1 == "child02"
    assert len(source[0][2]) == 2
    assert source[0][2].can_have_children()

    # Children of root 1
    assert source[1][0].val1 == "child10"
    assert len(source[1][0]) == 0
    assert not source[1][0].can_have_children()

    assert source[1][1].val1 == "child11"
    assert len(source[1][1]) == 0
    assert source[1][1].can_have_children()

    assert source[1][2].val1 == "child12"
    assert len(source[1][2]) == 2
    assert source[1][2].can_have_children()

    # If level 1 has all accessors, check them as well.
    if 1 in all_accessor_levels:
        assert source[0][0].val2 == 11
        assert source[0][1].val2 == 12
        assert source[0][2].val2 == 13

        assert source[1][0].val2 == 21
        assert source[1][1].val2 == 22
        assert source[1][2].val2 == 23

    # Children of root 0, child 2
    assert source[0][2][0].val1 == "child020"
    assert len(source[0][2][0]) == 0
    assert not source[0][2][0].can_have_children()

    assert source[0][2][1].val1 == "child021"
    assert len(source[0][2][1]) == 0
    assert not source[0][2][1].can_have_children()

    # Children of root 1, child 2
    assert source[1][2][0].val1 == "child120"
    assert len(source[1][2][0]) == 0
    assert not source[1][2][0].can_have_children()

    assert source[1][2][1].val1 == "child121"
    assert len(source[1][2][1]) == 0
    assert not source[1][2][1].can_have_children()

    # If level 2 has all accessors, check them as well.
    if 2 in all_accessor_levels:
        assert source[0][2][0].val2 == 131
        assert source[0][2][1].val2 == 132

        assert source[1][2][0].val2 == 231
        assert source[1][2][1].val2 == 232


def test_source_single_object():
    """A single object can be passed as root data."""
    source = TreeSource(accessors=["val1", "val2"], data="A string")

    assert len(source) == 1
    assert source[0].val1 == "A string"


def test_single_object_child():
    """A single object can be passed as child data."""
    source = TreeSource(
        accessors=["val1", "val2"],
        data={("root1", 1): "A string"},
    )

    assert len(source) == 1
    assert source[0].val1 == "root1"
    assert source[0].val2 == 1
    assert source[0].can_have_children()

    assert len(source[0]) == 1
    assert len(source[0][0]) == 0
    assert source[0][0].val1 == "A string"
    assert not source[0][0].can_have_children()


def test_modify_roots(source, listener):
    """The roots of a source can be modified."""
    root = source[1]
    assert root.val1 == "group2"

    # delete the root
    del source[1]

    # Removal notification was sent
    listener.remove.assert_called_once_with(parent=None, index=1, item=root)
    listener.reset_mock()

    # Root is no longer associated with the source
    assert root._parent is None
    assert root._source is None

    # Root count has dropped
    assert len(source) == 1

    old_root_0 = source[0]

    # A child can be modified by index
    source[0] = {"val1": "new"}

    # Root 0 has changed instance
    assert old_root_0 is not source[0]

    # Old child 0 is no longer associated with this node
    assert old_root_0._source is None
    assert old_root_0._parent is None

    # Change notification was sent, the change is associated with the new item
    listener.change.assert_called_once_with(item=source[0])

    # Source's root count hasn't changed
    assert len(source) == 1


def test_iter_root(source):
    """The roots of a source can be iterated over."""
    assert "|".join(root.val1 for root in source) == "group1|group2"


def test_clear(source, listener):
    """A TreeSource can be cleared."""
    source.clear()

    assert len(source) == 0

    # Clear notification was sent
    listener.clear.assert_called_once_with()


@pytest.mark.parametrize(
    "index, actual_index",
    [
        (1, 1),  # Positive, in range
        (10, 2),  # Positive, past positive limit
        (-1, 1),  # Negative, in range
        (-10, 0),  # Negative, past negative limit
    ],
)
def test_insert(source, listener, index, actual_index):
    """A new root node can be inserted."""
    new_child = source.insert(index, {"val1": "new"})

    # Source has one more root.
    assert len(source) == 3
    assert source[actual_index] == new_child

    # Root data is as expected
    assert source[actual_index].val1 == "new"

    # Insert notification was sent, the change is associated with the new item
    listener.insert.assert_called_once_with(
        parent=None,
        index=actual_index,
        item=new_child,
    )


def test_insert_with_children(source, listener):
    """A new root node can be inserted with children."""
    new_child = source.insert(
        1,
        {"val1": "new"},
        children=[
            ({"val1": "new child 1"}, None),
            ({"val1": "new child 2"}, None),
        ],
    )

    # Source has one more root.
    assert len(source) == 3
    assert source[1] == new_child

    # Root data is as expected
    assert source[1].val1 == "new"
    assert len(source[1]) == 2

    # Children are also present
    assert source[1][0].val1 == "new child 1"
    assert not source[1][0].can_have_children()
    assert source[1][1].val1 == "new child 2"
    assert not source[1][1].can_have_children()

    # Insert notification was sent, the change is associated with the new item
    listener.insert.assert_called_once_with(
        parent=None,
        index=1,
        item=new_child,
    )


def test_append(source, listener):
    """A new root node can be appended."""
    new_child = source.append({"val1": "new"})

    # Source has one more root.
    assert len(source) == 3
    assert source[2] == new_child

    # Root data is as expected
    assert source[2].val1 == "new"

    # Insert notification was sent, the change is associated with the new item
    listener.insert.assert_called_once_with(
        parent=None,
        index=2,
        item=new_child,
    )


def test_append_with_children(source, listener):
    """A new root node can be inserted with children."""
    new_child = source.append(
        {"val1": "new"},
        children=[
            ({"val1": "new child 1"}, None),
            ({"val1": "new child 2"}, None),
        ],
    )

    # Source has one more root.
    assert len(source) == 3
    assert source[2] == new_child

    # Root data is as expected
    assert source[2].val1 == "new"
    assert len(source[2]) == 2

    # Children are also present
    assert source[2][0].val1 == "new child 1"
    assert not source[2][0].can_have_children()
    assert source[2][1].val1 == "new child 2"
    assert not source[2][1].can_have_children()

    # Insert notification was sent, the change is associated with the new item
    listener.insert.assert_called_once_with(
        parent=None,
        index=2,
        item=new_child,
    )


def test_remove_root(source, listener):
    """A root node can be removed."""
    root = source[1]
    source.remove(root)

    # One less item in the source
    assert len(source) == 1

    # The root is no longer associated with the source
    assert root._source is None

    # Removal notification was sent
    listener.remove.assert_called_once_with(parent=None, index=1, item=root)


def test_remove_child(source, listener):
    """A child node can be removed from a source."""
    node = source[1][1]
    source.remove(node)

    # The source still has 2 roots
    assert len(source) == 2
    # ... but there's 1 less child
    assert len(source[1]) == 2

    # The child is no longer associated with the source,
    # and the child isn't associated with its parent.
    assert node._source is None
    assert node._parent is None

    # Removal notification was sent
    listener.remove.assert_called_once_with(parent=source[1], index=1, item=node)


def test_remove_non_root(source, listener):
    """If a node isn't associated with this source, remove raises an error."""
    other = Node(val="other")

    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .*> is not managed by this data source",
    ):
        source.remove(other)


def test_index(source):
    """A root can be found in a TreeSource."""
    root = source[1]
    assert source.index(root) == 1


def test_find(source):
    """A node can be found by value."""
    root1 = source[1]

    # Append some additional roots
    root2 = source.append({"val1": "group1", "val2": 333})
    root3 = source.append({"val1": "group2", "val2": 444})

    # Find the child by a partial match of values.
    assert source.find({"val1": "group2"}) == root1

    # Find the child by a partial match of values, starting at the first match
    assert source.find({"val1": "group2"}, start=root1) == root3

    # Find the child by a full match of values, starting at the first match
    assert source.find({"val1": "group1", "val2": 333}) == root2
