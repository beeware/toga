import pytest

import toga

from .test_command import assert_order


def test_create():
    """A group can be created with defaults."""
    grp = toga.Group("Group name")
    assert grp.text == "Group name"
    assert grp.order == 0

    assert repr(grp) == "<Group text='Group name' order=0>"


def test_create_with_params():
    """A fully specified group can be created."""
    parent = toga.Group("Parent name")
    grp = toga.Group("Group name", order=2, section=3, parent=parent)

    assert grp.text == "Group name"
    assert grp.order == 2
    assert grp.section == 3
    assert grp.parent == parent

    assert (
        repr(grp)
        == "<Group text='Group name' order=2 parent=<Group text='Parent name' order=0> section=3>"
    )


def test_create_section_without_parent():
    """A group cannot be created with a section but no parent."""
    with pytest.raises(
        ValueError,
        match=r"Section cannot be set without parent group",
    ):
        toga.Group("Group name", order=2, section=3)


def test_hashable():
    """Groups are hashable."""
    grp1 = toga.Group("text 1")
    grp2 = toga.Group("text 2")

    # The hash is based on the full path, not just the text.
    # This allows texts to be non-unique, as long as they're in
    # different groups
    grp1_child = toga.Group("text", parent=grp1)
    grp2_child = toga.Group("text", parent=grp2)

    # Insert the groups as keys in a dict. This is
    # only possible if Group is hashable.
    groups = {
        grp1: "First",
        grp2: "Second",
        grp1_child: "Child of 1",
        grp2_child: "Child of 2",
    }

    assert groups[grp1] == "First"
    assert groups[grp2] == "Second"
    assert groups[grp1_child] == "Child of 1"
    assert groups[grp2_child] == "Child of 2"


def test_group_eq():
    """Groups can be compared for equality."""
    group_a = toga.Group("A")
    group_b = toga.Group("B")
    group_a1 = toga.Group("A", order=1)
    # Assign None to variable to trick flake8 into not giving an E711
    other = None

    # Same instance is equal
    assert group_a == group_a
    assert group_a1 == group_a1

    # Same values are equal
    assert group_a == toga.Group("A")
    assert group_a1 == toga.Group("A", order=1)

    # Different values are not equal
    assert group_a != group_b
    assert group_a != other

    # Partially same values are not equal
    assert group_a1 != group_a
    assert group_a1 != toga.Group("B", order=1)
    assert group_a1 != toga.Group("A", order=2)


def test_parent_creation():
    """Parents can be assigned at creation."""
    group_a = toga.Group("A")
    group_b = toga.Group("B", parent=group_a)
    group_c = toga.Group("C", parent=group_b)

    # None checks
    assert not group_a.is_parent_of(None)
    assert not group_a.is_child_of(None)

    # Parent relationships
    assert group_a.is_parent_of(group_b)
    assert group_b.is_parent_of(group_c)
    assert group_a.is_parent_of(group_c)  # grandparent

    # Child relationships
    assert group_b.is_child_of(group_a)
    assert group_c.is_child_of(group_b)
    assert group_c.is_child_of(group_a)  # grandchild

    # Reverse direction relationships aren't true
    assert not group_a.is_child_of(group_b)
    assert not group_b.is_child_of(group_c)
    assert not group_a.is_child_of(group_c)

    assert not group_b.is_parent_of(group_a)
    assert not group_c.is_parent_of(group_b)
    assert not group_c.is_parent_of(group_a)

    assert group_a.parent is None
    assert group_a.root == group_a

    assert group_b.parent == group_a
    assert group_b.root == group_a

    assert group_c.parent == group_b
    assert group_c.root == group_a


def test_parent_assignment():
    """Parents can be assigned at runtime."""
    # Eventually, we'll end up with A->B->C, D.
    group_a = toga.Group("A")
    group_b = toga.Group("B")
    group_c = toga.Group("C")
    group_d = toga.Group("D")

    assert not group_a.is_parent_of(group_b)
    assert not group_b.is_parent_of(group_c)
    assert not group_a.is_parent_of(group_c)
    assert not group_b.is_parent_of(group_d)
    assert not group_a.is_parent_of(group_d)

    assert not group_b.is_child_of(group_a)
    assert not group_c.is_child_of(group_b)
    assert not group_c.is_child_of(group_a)
    assert not group_d.is_child_of(group_b)
    assert not group_d.is_child_of(group_a)

    assert not group_a.is_child_of(group_b)
    assert not group_b.is_child_of(group_c)
    assert not group_a.is_child_of(group_c)
    assert not group_b.is_child_of(group_d)
    assert not group_a.is_child_of(group_d)

    assert not group_b.is_parent_of(group_a)
    assert not group_c.is_parent_of(group_b)
    assert not group_c.is_parent_of(group_a)
    assert not group_d.is_parent_of(group_b)
    assert not group_d.is_parent_of(group_a)

    assert group_a.parent is None
    assert group_a.root == group_a

    assert group_b.parent is None
    assert group_b.root == group_b

    assert group_c.parent is None
    assert group_c.root == group_c

    # Assign parents.
    # C is assigned to B *before* B is assigned to A.
    # D is assigned to B *after* B is assigned to A.
    # This ensures that root isn't preserved in an intermediate state
    group_c.parent = group_b
    group_b.parent = group_a
    group_d.parent = group_b

    assert group_a.is_parent_of(group_b)
    assert group_b.is_parent_of(group_c)
    assert group_a.is_parent_of(group_c)  # grandparent
    assert group_b.is_parent_of(group_d)
    assert group_a.is_parent_of(group_d)  # grandparent

    assert group_b.is_child_of(group_a)
    assert group_c.is_child_of(group_b)
    assert group_c.is_child_of(group_a)  # grandchild
    assert group_d.is_child_of(group_b)
    assert group_d.is_child_of(group_a)  # grandchild

    # Reverse direction relationships aren't true
    assert not group_a.is_child_of(group_b)
    assert not group_b.is_child_of(group_c)
    assert not group_a.is_child_of(group_c)
    assert not group_b.is_child_of(group_d)
    assert not group_a.is_child_of(group_d)

    assert not group_b.is_parent_of(group_a)
    assert not group_c.is_parent_of(group_b)
    assert not group_c.is_parent_of(group_a)
    assert not group_d.is_parent_of(group_b)
    assert not group_d.is_parent_of(group_a)

    assert group_a.parent is None
    assert group_a.root == group_a

    assert group_b.parent == group_a
    assert group_b.root == group_a

    assert group_c.parent == group_b
    assert group_c.root == group_a

    assert group_d.parent == group_b
    assert group_d.root == group_a


def test_parent_loops():
    """Parent loops are prevented can be assigned at runtime."""
    group_a = toga.Group("A")
    group_b = toga.Group("B", parent=group_a)
    group_c = toga.Group("C", parent=group_b)

    #
    with pytest.raises(
        ValueError,
        match=r"A group cannot be it's own parent",
    ):
        group_a.parent = group_a

    with pytest.raises(
        ValueError,
        match=r"Cannot set parent; 'A' is an ancestor of 'B'.",
    ):
        group_a.parent = group_b

    with pytest.raises(
        ValueError,
        match=r"Cannot set parent; 'A' is an ancestor of 'C'.",
    ):
        group_a.parent = group_c


def test_order_by_text():
    """Groups are ordered by text if order and section are equivalent."""
    assert_order(toga.Group("A"), toga.Group("B"))


def test_order_by_number():
    """Groups are ordered by number."""
    assert_order(toga.Group("B", order=1), toga.Group("A", order=2))


def test_order_by_groups(parent_group_1, parent_group_2):
    """Groups are ordered by parent, then section, then order."""
    assert_order(
        parent_group_1,
        toga.Group("C", parent=parent_group_1),
        toga.Group("D", parent=parent_group_1),
        toga.Group("AA3", parent=parent_group_1, section=2),
        toga.Group("AA2", parent=parent_group_1, section=3, order=1),
        toga.Group("AA1", parent=parent_group_1, section=3, order=2),
        parent_group_2,
        toga.Group("B", parent=parent_group_2),
    )


# def test_cannot_set_self_as_parent(self):
#     group = toga.Group("P")
#     with self.assertRaises(ValueError):
#         group.parent = group
#     self.assert_parent_and_root(group, None, group)


# def test_cannot_set_child_to_be_a_parent_of_its_grandparent(self):
#     grandparent = toga.Group("G")
#     parent = toga.Group("P", parent=grandparent)
#     child = toga.Group("C", parent=parent)
#     with self.assertRaises(ValueError):
#         grandparent.parent = child
#     self.assert_parent_and_root(grandparent, None, grandparent)
#     self.assert_parent_and_root(parent, grandparent, grandparent)
#     self.assert_parent_and_root(child, parent, grandparent)


# def assert_parent_and_root(self, group, parent, root):
#     self.assertEqual(group.parent, parent)
#     self.assertEqual(group.root, root)
