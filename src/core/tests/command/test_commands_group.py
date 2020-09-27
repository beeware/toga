import unittest

import toga
from tests.utils import order_test

from tests.command.constants import PARENT_GROUP1, PARENT_GROUP2


class TestCommandsGroup(unittest.TestCase):

    def test_group_init_no_order(self):
        grp = toga.Group('label')
        self.assertEqual(grp.label, 'label')
        self.assertEqual(grp.order, 0)

    def test_group_init_with_order(self):
        grp = toga.Group('label', 2)
        self.assertEqual(grp.label, 'label')
        self.assertEqual(grp.order, 2)

    def test_group_eq(self):
        self.assertEqual(toga.Group('A'), toga.Group('A'))
        self.assertEqual(toga.Group('A', 1), toga.Group('A', 1))
        self.assertNotEqual(toga.Group('A'), toga.Group('B'))
        self.assertNotEqual(toga.Group('A', 1), toga.Group('A', 2))
        self.assertNotEqual(toga.Group('A', 1), toga.Group('B', 1))

    def test_set_parent_in_constructor(self):
        parent = toga.Group("parent")
        child = toga.Group("child", parent=parent)
        self.assert_parent_and_children(parent, None, [child])
        self.assert_parent_and_children(child, parent, [])

    def test_set_parent_in_property(self):
        parent = toga.Group("parent")
        child = toga.Group("child")
        child.parent = parent
        self.assert_parent_and_children(parent, None, [child])
        self.assert_parent_and_children(child, parent, [])

    def test_set_children_in_constructor(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent", children=[child1, child2])
        self.assert_parent_and_children(parent, None, [child1, child2])
        self.assert_parent_and_children(child1, parent, [])
        self.assert_parent_and_children(child2, parent, [])

    def test_set_children_in_property(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent")
        parent.children = [child1, child2]
        self.assert_parent_and_children(parent, None, [child1, child2])
        self.assert_parent_and_children(child1, parent, [])
        self.assert_parent_and_children(child2, parent, [])

    def test_add_child(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent", children=[child1])
        parent.add_child(child2)
        self.assert_parent_and_children(parent, None, [child1, child2])
        self.assert_parent_and_children(child1, parent, [])
        self.assert_parent_and_children(child2, parent, [])

    def test_remove_child(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent", children=[child1, child2])
        parent.remove_child(child1)
        self.assert_parent_and_children(parent, None, [child2])
        self.assert_parent_and_children(child1, None, [])
        self.assert_parent_and_children(child2, parent, [])

    def test_add_child_twice_in_constructor(self):
        child = toga.Group("child")
        parent = toga.Group("parent", children=[child, child])
        self.assert_parent_and_children(parent, None, [child])
        self.assert_parent_and_children(child, parent, [])

    def test_change_children_after_initialize(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        child3 = toga.Group("child3")
        parent = toga.Group("parent", children=[child1, child2])
        parent.children = [child2, child3]
        self.assert_parent_and_children(parent, None, [child2, child3])
        self.assert_parent_and_children(child1, None, [])
        self.assert_parent_and_children(child2, parent, [])
        self.assert_parent_and_children(child3, parent, [])

    def test_change_parent(self):
        child = toga.Group("child")
        parent1 = toga.Group("parent1", children=[child])
        parent2 = toga.Group("parent2")
        child.parent = parent2
        self.assert_parent_and_children(parent1, None, [])
        self.assert_parent_and_children(parent2, None, [child])
        self.assert_parent_and_children(child, parent2, [])

    def test_groups_inheritance(self):
        top = toga.Group("C")
        middle = toga.Group("B", parent=top)
        bottom = toga.Group("A", parent=middle)
        groups = [top, middle, bottom]
        for i in range(0, 2):
            for j in range(i + 1, 3):
                self.assertTrue(groups[i].is_parent_of(groups[j]))
                self.assertTrue(groups[j].is_child_of(groups[i]))

    test_order_by_number = order_test(toga.Group('A', 1), toga.Group('A', 2))
    test_order_ignore_label = order_test(toga.Group('B', 1), toga.Group('A', 2))
    test_order_by_label = order_test(toga.Group('A'), toga.Group('B'))
    test_order_by_groups = order_test(
        PARENT_GROUP1,
        toga.Group('C', parent=PARENT_GROUP1),
        toga.Group('D', parent=PARENT_GROUP1),
        toga.Group('A', parent=PARENT_GROUP1, section=2),
        PARENT_GROUP2,
        toga.Group("B", parent=PARENT_GROUP2),
    )

    def test_group_repr(self):
        parent = toga.Group("P")
        self.assertEqual(
            repr(toga.Group("A")), "Group[label=A, order=0, parent=None, children=[]]"
        )
        self.assertEqual(
            repr(toga.Group("A", parent=parent)),
            "Group[label=A, order=0, parent=P, children=[]]"
        )
        self.assertEqual(
            repr(toga.Group("A", children=[toga.Group("B"), toga.Group("C")])),
            "Group[label=A, order=0, parent=None, children=[B, C]]"
        )

    def test_set_section_without_parent(self):
        with self.assertRaises(ValueError):
            toga.Group("A", section=2)

    def test_set_parent_causes_cyclic_parenting(self):
        parent = toga.Group("P")
        child = toga.Group("C", parent=parent)
        with self.assertRaises(ValueError):
            parent.parent = child
        self.assert_parent_and_children(parent, None, [child])
        self.assert_parent_and_children(child, parent, [])

    def test_set_children_causes_cyclic_parenting(self):
        parent = toga.Group("P")
        child1 = toga.Group("C", parent=parent)
        child2 = toga.Group("D")
        with self.assertRaises(ValueError):
            child1.children = [parent, child2]
        self.assert_parent_and_children(parent, None, [child1])
        self.assert_parent_and_children(child1, parent, [])
        self.assert_parent_and_children(child2, None, [])

    def test_add_child_causes_cyclic_parenting(self):
        parent = toga.Group("P")
        child = toga.Group("C", parent=parent)
        with self.assertRaises(ValueError):
            child.add_child(parent)
        self.assert_parent_and_children(parent, None, [child])
        self.assert_parent_and_children(child, parent, [])

    def test_cannot_set_self_as_parent(self):
        group = toga.Group("P")
        with self.assertRaises(ValueError):
            group.parent = group
        self.assert_parent_and_children(group, None, [])

    def test_cannot_set_self_as_child(self):
        group = toga.Group("P")
        child = toga.Group("C")
        with self.assertRaises(ValueError):
            group.children = [group, child]
        self.assert_parent_and_children(group, None, [])
        self.assert_parent_and_children(child, None, [])

    def test_cannot_add_self_as_child(self):
        parent = toga.Group("P")
        with self.assertRaises(ValueError):
            parent.add_child(parent)
        self.assert_parent_and_children(parent, None, [])

    def test_cannot_set_child_to_be_a_parent_of_its_grandparent(self):
        grandparent = toga.Group("G")
        parent = toga.Group("P", parent=grandparent)
        child = toga.Group("C", parent=parent)
        with self.assertRaises(ValueError):
            grandparent.parent = child
        self.assert_parent_and_children(grandparent, None, [parent])
        self.assert_parent_and_children(parent, grandparent, [child])
        self.assert_parent_and_children(child, parent, [])

    def assert_parent_and_children(self, group, parent, children):
        self.assertEqual(group.parent, parent)
        self.assertEqual(group.children, children)
