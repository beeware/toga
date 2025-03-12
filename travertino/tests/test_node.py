from unittest.mock import Mock, call
from warnings import catch_warnings, filterwarnings

import pytest

from travertino.layout import BaseBox, Viewport
from travertino.node import Node
from travertino.properties.validated import validated_property
from travertino.size import BaseIntrinsicSize
from travertino.style import BaseStyle

from .utils import apply_dataclass, mock_apply


@mock_apply
@apply_dataclass
class Style(BaseStyle):
    int_prop: int = validated_property(integer=True)

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, viewport):
        # A simple layout scheme that allocates twice the viewport size.
        self._applicator.node.layout.content_width = viewport.width * 2
        self._applicator.node.layout.content_height = viewport.height * 2


@mock_apply
@apply_dataclass
class OldStyle(Style):
    # Uses two-argument layout(), as in Toga <= 0.4.8
    def layout(self, node, viewport):
        # A simple layout scheme that allocates twice the viewport size.
        super().layout(viewport)


@mock_apply
@apply_dataclass
class TypeErrorStyle(Style):
    # Uses the correct signature, but raises an unrelated TypeError in layout
    def layout(self, viewport):
        raise TypeError("An unrelated TypeError has occurred somewhere in layout()")


@mock_apply
@apply_dataclass
class OldTypeErrorStyle(Style):
    # Just to be extra safe...
    def layout(self, node, viewport):
        raise TypeError("An unrelated TypeError has occurred somewhere in layout()")


@apply_dataclass
class BrokenStyle(BaseStyle):
    def apply(self):
        raise AttributeError("Missing attribute, node not ready for style application")

    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def layout(self, viewport):
        # A simple layout scheme that allocates twice the viewport size.
        self._applicator.node.layout.content_width = viewport.width * 2
        self._applicator.node.layout.content_height = viewport.height * 2


@apply_dataclass
class AttributeTestStyle(BaseStyle):
    class IntrinsicSize(BaseIntrinsicSize):
        pass

    class Box(BaseBox):
        pass

    def apply(self):
        assert self._applicator.node.style is self


def test_create_leaf():
    """A leaf can be created"""
    style = Style()
    leaf = Node(style=style)

    assert leaf._children is None
    assert leaf.children == []
    assert not leaf.can_have_children

    # An unattached leaf is a root
    assert leaf.parent is None
    assert leaf.root == leaf

    # A leaf can't have children
    child = Node(style=style)

    with pytest.raises(ValueError):
        leaf.add(child)


def test_create_node():
    """A node can be created with children"""
    style = Style()

    child1 = Node(style=style)
    child2 = Node(style=style)
    child3 = Node(style=style)

    node = Node(style=style, children=[child1, child2, child3])

    assert node.children == [child1, child2, child3]
    assert node.can_have_children

    # The node is the root as well.
    assert node.parent is None
    assert node.root == node

    # The children all point at the node.
    assert child1.parent == node
    assert child1.root == node

    assert child2.parent == node
    assert child2.root == node

    assert child3.parent == node
    assert child3.root == node

    # Create another node
    new_node = Node(style=style, children=[])

    assert new_node.children == []
    assert new_node.can_have_children

    # Add the old node as a child of the new one.
    new_node.add(node)

    # The new node is the root
    assert new_node.parent is None
    assert new_node.root == new_node

    # The node is the root as well.
    assert node.parent == new_node
    assert node.root == new_node

    # The children all point at the node.
    assert child1.parent == node
    assert child1.root == new_node

    assert child2.parent == node
    assert child2.root == new_node

    assert child3.parent == node
    assert child3.root == new_node


@pytest.mark.parametrize("StyleClass", [Style, OldStyle])
def test_refresh(StyleClass):
    """The layout can be refreshed, and the applicator invoked"""

    # Define an applicator that tracks the node being rendered and its size
    class Applicator:
        def __init__(self, node):
            self.tasks = []
            self.node = node

        def set_bounds(self):
            self.tasks.append(
                (
                    self.node,
                    self.node.layout.content_width,
                    self.node.layout.content_height,
                )
            )

    class TestNode(Node):
        def __init__(self, style, children=None):
            super().__init__(
                style=style, applicator=Applicator(self), children=children
            )

    # Define a simple 2 level tree of nodes.
    style = StyleClass()
    child1 = TestNode(style=style)
    child2 = TestNode(style=style)
    child3 = TestNode(style=style)

    node = TestNode(style=style, children=[child1, child2, child3])

    # Refresh the root node
    node.refresh(Viewport(width=10, height=20))

    # Check the output is as expected
    assert node.applicator.tasks == [(node, 20, 40)]
    assert child1.applicator.tasks == []
    assert child2.applicator.tasks == []
    assert child3.applicator.tasks == []

    # Reset the applicator
    node.applicator.tasks = []

    # Refresh a child node
    child1.refresh(Viewport(width=15, height=25))

    # The root node was rendered, not the child.
    assert node.applicator.tasks == [(node, 30, 50)]
    assert child1.applicator.tasks == []
    assert child2.applicator.tasks == []
    assert child3.applicator.tasks == []


def test_refresh_no_op():
    """Refresh is a no-op if no applicator is set."""
    node = Node(style=Style())
    node.refresh(Viewport(width=100, height=100))
    node.style.apply.assert_not_called()


@pytest.mark.parametrize("StyleClass", [TypeErrorStyle, OldTypeErrorStyle])
def test_type_error_in_layout(StyleClass):
    """The shim shouldn't hide unrelated TypeErrors."""

    class Applicator:
        def set_bounds(self):
            pass

    node = Node(style=StyleClass(), applicator=Applicator())
    with pytest.raises(TypeError, match=r"unrelated TypeError"):
        node.refresh(Viewport(50, 50))


def test_add():
    """Nodes can be added as children to another node"""

    style = Style()
    node = Node(style=style, children=[])

    child = Node(style=style)
    node.add(child)

    assert child in node.children
    assert child.parent == node
    assert child.root == node.root


def test_insert():
    """Node can be inserted at a specific position as a child"""

    style = Style()
    child1 = Node(style=style)
    child2 = Node(style=style)
    child3 = Node(style=style)
    node = Node(style=style, children=[child1, child2, child3])

    child4 = Node(style=style)

    index = 2
    node.insert(index, child4)

    assert child4 in node.children
    assert child4.parent == node
    assert child4.root == node.root

    assert node.children.index(child4) == index


def test_insert_leaf():
    """Node that can't contain children raises error on insert."""
    node = Node(style=Style())
    child = Node(style=Style())
    with pytest.raises(ValueError, match=r"Cannot insert child"):
        node.insert(0, child)


def test_remove():
    """Children can be removed from node"""

    style = Style()
    child1 = Node(style=style)
    child2 = Node(style=style)
    child3 = Node(style=style)
    node = Node(style=style, children=[child1, child2, child3])

    node.remove(child1)

    assert child1 not in node.children
    assert child1.parent is None
    assert child1.root == child1


def test_remove_leaf():
    """Node that can't contain children raises error on remove."""
    node = Node(style=Style())
    child = Node(style=Style())
    with pytest.raises(ValueError, match=r"Cannot remove children"):
        node.remove(child)


def test_clear():
    """Node can be cleared of all children."""
    style = Style()
    children = [Node(style=style), Node(style=style), Node(style=style)]
    node = Node(style=style, children=children)

    for child in children:
        assert child in node.children
        assert child.parent == node
        assert child.root == node
    assert node.children == children

    node.clear()

    for child in children:
        assert child not in node.children
        assert child.parent is None
        assert child.root == child

    assert node.children == []


def test_clear_leaf():
    """For a node that can't have children, clear() is a no-op."""
    node = Node(style=Style())
    assert node.children == []
    node.clear()
    assert node.children == []


def test_create_with_no_applicator():
    """A node can be created without an applicator."""
    style = Style(int_prop=5)
    node = Node(style=style)

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style
    assert node.style.int_prop == 5
    assert node.style is not style

    # Since no applicator has been assigned, the overall style wasn't applied. However,
    # apply("int_prop") was still called.
    node.style.apply.assert_called_once_with("int_prop")


def test_create_with_applicator():
    """A node can be created with an applicator."""
    style = Style(int_prop=5)
    applicator = Mock()
    node = Node(style=style, applicator=applicator)

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style
    assert node.style.int_prop == 5
    assert node.style is not style

    # Applicator assignment does *not* copy.
    assert node.applicator is applicator
    # Applicator gets a reference back to its node and to the style.
    assert applicator.node is node
    assert node.style._applicator is applicator

    # First, call("int_prop") is called when style object is created.
    # Assigning a non-None applicator should always apply style.
    assert node.style.apply.mock_calls == [call("int_prop"), call()]


@pytest.mark.parametrize(
    "node",
    [
        Node(style=Style()),
        Node(style=Style(), applicator=Mock()),
    ],
)
def test_assign_applicator(node):
    """A node can be assigned an applicator after creation."""
    node.style.apply.reset_mock()

    applicator = Mock()
    node.applicator = applicator

    # Applicator assignment does *not* copy.
    assert node.applicator is applicator
    # Applicator gets a reference back to its node and to the style.
    assert applicator.node is node
    assert node.style._applicator is applicator

    # Assigning a non-None applicator should always apply style.
    node.style.apply.assert_called_once_with()


@pytest.mark.parametrize(
    "node",
    [
        Node(style=Style()),
        Node(style=Style(), applicator=Mock()),
    ],
)
def test_assign_applicator_none(node):
    """A node can have its applicator set to None."""
    node.style.apply.reset_mock()

    node.applicator = None
    assert node.applicator is None

    # Should be updated on style as well
    assert node.style._applicator is None
    # Assigning None to applicator does not trigger apply.
    node.style.apply.assert_not_called()


def assign_new_applicator():
    """Assigning a new applicator clears reference to node on the old applicator."""
    applicator_1 = Mock()
    node = Node(style=Style(), applicator=applicator_1)

    assert applicator_1.node is node

    applicator_2 = Mock()
    node.applicator = applicator_2

    assert applicator_1.node is None
    assert applicator_2.node is node


def assign_new_applicator_none():
    """Assigning None to applicator clears reference to node on the old applicator."""
    applicator = Mock()
    node = Node(style=Style(), applicator=applicator)

    assert applicator.node is node

    node.applicator = None

    assert applicator.node is None


def test_assign_style_with_applicator():
    """Assigning a new style triggers an apply if an applicator is already present."""
    style_1 = Style(int_prop=5)
    node = Node(style=style_1, applicator=Mock())

    style_2 = Style(int_prop=10)
    node.style = style_2

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style_2
    assert node.style.int_prop == 10
    assert node.style is not style_2

    assert node.style != style_1

    # call("int_prop") is called when the style object is created.
    # Since an applicator has already been assigned, assigning style applies the style.
    assert node.style.apply.mock_calls == [call("int_prop"), call()]


def test_assign_style_with_no_applicator():
    """Assigning new style doesn't trigger an apply if an applicator isn' present."""
    style_1 = Style(int_prop=5)
    node = Node(style=style_1)

    style_2 = Style(int_prop=10)
    node.style = style_2

    # Style copies on assignment.
    assert isinstance(node.style, Style)
    assert node.style == style_2
    assert node.style.int_prop == 10
    assert node.style is not style_2

    assert node.style != style_1

    # Since no applicator has been assigned, the overall style wasn't applied. However,
    # apply("int_prop") was still called when creating the style.
    node.style.apply.assert_called_once_with("int_prop")


def test_apply_before_node_is_ready():
    """Triggering an apply raises a warning if the node is not ready to apply style."""
    style = BrokenStyle()
    applicator = Mock()

    with pytest.warns(RuntimeWarning):
        node = Node(style=style)
        node.applicator = applicator

    with pytest.warns(RuntimeWarning):
        node.style = BrokenStyle()

    with pytest.warns(RuntimeWarning):
        Node(style=style, applicator=applicator)


def test_applicator_has_node_reference():
    """Applicator should have a reference to its node before style is first applied."""

    # We can't just check it after creating the widget, because at that point the
    # apply will have already happened. AttributeTestStyle has an apply() method
    # that asserts the reference trail of style -> applicator -> node -> style is
    # already intact at the point that apply is called.

    with catch_warnings():
        filterwarnings("error", category=RuntimeWarning)
        Node(style=AttributeTestStyle(), applicator=Mock())
