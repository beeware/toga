import re
from unittest.mock import Mock

import pytest

from toga.sources import Node


def _create_node(source, parent, data, children=None):
    """A very simplified _create_node for mock purposes."""
    node = Node(**data)
    node._source = source
    node._parent = parent
    if children:
        node._children = [
            _create_node(source, parent=node, data=item[0], children=item[1])
            for item in children
        ]
    return node


@pytest.fixture
def source():
    source = Mock()
    source._accessors = ["val1", "val2"]
    source._create_node.side_effect = lambda *args, **kwargs: _create_node(
        source, *args, **kwargs
    )
    return source


@pytest.fixture
def leaf_node(source):
    node = Node(val1="value 1", val2=42)
    node._source = source
    return node


@pytest.fixture
def empty_node(source):
    node = Node()
    node._source = source
    node._children = []
    return node


@pytest.fixture
def child_a(source, leaf_node):
    child = Node(val1="value a", val2=111)
    child._source = source
    child._parent = leaf_node
    return child


@pytest.fixture
def child_b(source, leaf_node):
    child = Node(val1="value b", val2=222)
    child._source = source
    child._parent = leaf_node
    return child


@pytest.fixture
def node(leaf_node, child_a, child_b):
    leaf_node._children = [child_a, child_b]

    return leaf_node


def test_node_properties(node):
    """A node with children can be created and modified."""
    assert node.val1 == "value 1"
    assert node.val2 == 42
    assert node.can_have_children()
    assert len(node) == 2
    assert (
        re.match(r"<Node .* val1='value 1' val2=42; 2 children>", repr(node))
        is not None
    )


def test_empty_node_properties(empty_node):
    """An empty Node can be created."""
    assert empty_node.can_have_children()
    assert len(empty_node) == 0
    assert (
        re.match(r"<Node .* \(no attributes\); 0 children>", repr(empty_node))
        is not None
    )


def test_leaf_node_properties(leaf_node):
    """A Leaf Node can be created."""
    assert leaf_node.val1 == "value 1"
    assert leaf_node.val2 == 42
    assert not leaf_node.can_have_children()
    assert len(leaf_node) == 0
    assert (
        re.match(r"<Leaf Node .* val1='value 1' val2=42>", repr(leaf_node)) is not None
    )


def test_modify_attributes(source, node):
    """If node attributes are modified, a change notification is sent."""
    node.val1 = "new value"
    assert node.val1 == "new value"
    source.notify.assert_called_once_with("change", item=node)
    source.notify.reset_mock()

    # Deleting an attribute causes a change notification
    del node.val1
    assert not hasattr(node, "val1")
    source.notify.assert_called_once_with("change", item=node)
    source.notify.reset_mock()

    # Setting an attribute starting with with an underscore isn't a notifiable event
    node._secret = "secret value"
    assert node._secret == "secret value"
    source.notify.assert_not_called()

    # Deleting an attribute starting with with an underscore isn't a notifiable event
    del node._secret
    assert not hasattr(node, "_secret")
    source.notify.assert_not_called()

    # An attribute that wasn't in the original attribute set
    # still causes a change notification
    node.val3 = "other value"
    assert node.val3 == "other value"
    source.notify.assert_called_once_with("change", item=node)
    source.notify.reset_mock()

    # Deleting an attribute that wasn't in the original attribute set
    # still causes a change notification
    del node.val3
    assert not hasattr(node, "val3")
    source.notify.assert_called_once_with("change", item=node)
    source.notify.reset_mock()


def test_modify_attributes_no_source(node):
    """Node attributes can be modified on a node with no source."""
    node.source = None

    node.val1 = "new value"
    assert node.val1 == "new value"

    # Deleting an attribute causes a change notification
    del node.val1
    assert not hasattr(node, "val1")

    # Setting an attribute starting with with an underscore isn't a notifiable event
    node._secret = "secret value"
    assert node._secret == "secret value"

    # Deleting an attribute starting with with an underscore isn't a notifiable event
    del node._secret
    assert not hasattr(node, "_secret")

    # An attribute that wasn't in the original attribute set
    # still causes a change notification
    node.val3 = "other value"
    assert node.val3 == "other value"

    # Deleting an attribute that wasn't in the original attribute set
    # still causes a change notification
    del node.val3
    assert not hasattr(node, "val3")


def test_modify_children(source, node):
    """Node children can be retrieved and modified."""
    child = node[1]
    assert node[1].val1 == "value b"

    # Delete the child
    del node[1]

    # Removal notification was sent
    source.notify.assert_called_once_with("remove", parent=node, index=1, item=child)
    source.notify.reset_mock()

    # Child is no longer associated with the source
    assert child._parent is None
    assert child._source is None

    # Node child count has dropped
    assert len(node) == 1

    old_child_0 = node[0]

    # A child can be modified by index
    node[0] = {"val1": "new"}

    # Node 0 has changed instance
    assert old_child_0 is not node[0]

    # Old child 0 is no longer associated with this node
    assert old_child_0._source is None
    assert old_child_0._parent is None

    # A child node was created using the source's factory
    source._create_node.assert_called_with(parent=node, data={"val1": "new"})

    # Change notification was sent, the change is associated with the new item
    source.notify.assert_called_once_with("change", item=node[0])

    # Node child count hasn't changed
    assert len(node) == 1


def test_modify_leaf_children(leaf_node):
    """Attempts to modifying Leaf Node children raise an error."""
    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .*> is a leaf node",
    ):
        leaf_node[1]

    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .*> is a leaf node",
    ):
        del leaf_node[1]

    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .*> is a leaf node",
    ):
        leaf_node[1] = {"val1": "new"}


def test_iterate(node):
    """Node can be iterated."""
    assert "|".join(child.val1 for child in node) == "value a|value b"


def test_iterate_leaf(leaf_node):
    """Node can be iterated."""
    assert "|".join(child.val1 for child in leaf_node) == ""


@pytest.mark.parametrize(
    "index, actual_index",
    [
        (1, 1),  # Positive, in range
        (10, 2),  # Positive, past positive limit
        (-1, 1),  # Negative, in range
        (-10, 0),  # Negative, past negative limit
    ],
)
def test_insert(source, node, index, actual_index):
    """A child can be inserted into a node."""
    new_child = node.insert(index, {"val1": "new"})

    # Node has one more child.
    assert len(node) == 3
    assert node[actual_index] == new_child

    # A child node was created using the source's factory
    source._create_node.assert_called_with(
        parent=node, data={"val1": "new"}, children=None
    )

    # insert notification was sent, the change is associated with the new item
    source.notify.assert_called_once_with(
        "insert",
        parent=node,
        index=actual_index,
        item=new_child,
    )


def test_insert_with_children(source, node):
    """A child with children can be inserted into a node."""
    new_child = node.insert(
        1,
        {"val1": "new"},
        children=[
            ({"val1": "new child 1"}, None),
            ({"val1": "new child 2"}, None),
        ],
    )

    # Node has one more child.
    assert len(node) == 3
    assert node[1] == new_child

    # A child node was created using the source's factory, and the child data was passed
    # to that call.
    source._create_node.assert_called_with(
        parent=node,
        data={"val1": "new"},
        children=[
            ({"val1": "new child 1"}, None),
            ({"val1": "new child 2"}, None),
        ],
    )

    # The children of the new child are as expected
    assert len(new_child) == 2
    assert new_child[0].val1 == "new child 1"
    assert not new_child[0].can_have_children()

    # insert notification was sent, the change is associated with the new item
    source.notify.assert_called_once_with(
        "insert",
        parent=node,
        index=1,
        item=new_child,
    )


def test_insert_leaf(leaf_node, source):
    """Inserting a child into a leaf makes the node not a leaf any more."""
    new_child = leaf_node.insert(0, {"val1": "new"})

    # Leaf node isn't a leaf any more
    assert leaf_node.can_have_children()
    assert len(leaf_node) == 1
    assert leaf_node[0] == new_child

    # A child node was created using the source's factory
    source._create_node.assert_called_with(
        parent=leaf_node, data={"val1": "new"}, children=None
    )

    # insert notification was sent, the change is associated with the new item
    source.notify.assert_called_once_with(
        "insert", parent=leaf_node, index=0, item=leaf_node[0]
    )


def test_append(source, node):
    """A child can be appended onto a node."""
    new_child = node.append({"val1": "new"})

    # Node has one more child.
    assert len(node) == 3
    assert node[2] == new_child

    # A child node was created using the source's factory
    source._create_node.assert_called_with(
        parent=node, data={"val1": "new"}, children=None
    )

    # insert notification was sent, the change is associated with the new item
    source.notify.assert_called_once_with(
        "insert",
        parent=node,
        index=2,
        item=new_child,
    )


def test_append_with_children(source, node):
    """A child with children can be appended onto a node."""
    new_child = node.append(
        {"val1": "new"},
        children=[
            ({"val1": "new child 1"}, None),
            ({"val1": "new child 2"}, None),
        ],
    )

    # Node has one more child.
    assert len(node) == 3
    assert node[2] == new_child

    # A child node was created using the source's factory, and the child data was passed
    # to that call. Since our source is a mock, we won't get actual children.
    source._create_node.assert_called_with(
        parent=node,
        data={"val1": "new"},
        children=[
            ({"val1": "new child 1"}, None),
            ({"val1": "new child 2"}, None),
        ],
    )

    # insert notification was sent, the change is associated with the new item
    source.notify.assert_called_once_with(
        "insert",
        parent=node,
        index=2,
        item=new_child,
    )


def test_append_leaf(leaf_node, source):
    """Appending to a leaf makes the node not a leaf any more."""
    new_child = leaf_node.append({"val1": "new"})

    # Leaf node isn't a leaf any more
    assert leaf_node.can_have_children()
    assert len(leaf_node) == 1
    assert leaf_node[0] == new_child

    # A child node was created using the source's factory
    source._create_node.assert_called_with(
        parent=leaf_node, data={"val1": "new"}, children=None
    )

    # insert notification was sent, the change is associated with the new item
    source.notify.assert_called_once_with(
        "insert", parent=leaf_node, index=0, item=leaf_node[0]
    )


def test_index(node, child_b):
    """A child can be found it it's parent."""
    assert node.index(child_b) == 1


def test_index_not_child(node):
    """If a node isn't a child of this node, it can't be found by index."""
    other = Node(val1="other")

    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .* val1='other'> is not in list",
    ):
        node.index(other)


def test_index_leaf(leaf_node, child_b):
    """A child cannot be found in a leaf node."""
    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .* val1='value 1' val2=42> is a leaf node",
    ):
        leaf_node.index(child_b)


def test_remove(source, node, child_b):
    """A node can be removed from it's parent."""
    # Child is initially associated with the node
    assert child_b._parent == node
    assert child_b._source == node._source

    # Remove the child
    node.remove(child_b)

    # Child isn't associated with the node any more
    assert child_b._parent is None
    assert child_b._source is None

    # The node has less children
    assert len(node) == 1

    # The source was notified
    source.notify.assert_called_once_with("remove", parent=node, index=1, item=child_b)


def test_remove_leaf(leaf_node, child_b):
    """A child cannot be removed from a leaf node."""
    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .* val1='value 1' val2=42> is a leaf node",
    ):
        leaf_node.index(child_b)


def test_find(node, child_b):
    """A node can be found by value in it's parent's list of children."""
    # Append some additional children
    child_c = node.append({"val1": "value a", "val2": 333})
    child_d = node.append({"val1": "value b", "val2": 444})

    # Find the child by a partial match of values.
    assert node.find({"val1": "value b"}) == child_b

    # Find the child by a partial match of values, starting at the first match
    assert node.find({"val1": "value b"}, start=child_b) == child_d

    # Find the child by a full match of values, starting at the first match
    assert node.find({"val1": "value a", "val2": 333}) == child_c


def test_found_leaf(leaf_node):
    """A child cannot be found from a leaf node."""
    with pytest.raises(
        ValueError,
        match=r"<Leaf Node .* val1='value 1' val2=42> is a leaf node",
    ):
        leaf_node.find({"val1": "value 1"})
