import unittest

import toga


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
        self.assertEqual(child.parent, parent)
        self.assertEqual(parent.children, [child])

    def test_set_parent_in_property(self):
        parent = toga.Group("parent")
        child = toga.Group("child")
        child.parent = parent
        self.assertEqual(child.parent, parent)
        self.assertEqual(parent.children, [child])

    def test_set_children_in_constructor(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent", children=[child1, child2])
        self.assertEqual(child1.parent, parent)
        self.assertEqual(child2.parent, parent)
        self.assertEqual(parent.children, [child1, child2])

    def test_set_children_in_property(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent")
        parent.children = [child1, child2]
        self.assertEqual(child1.parent, parent)
        self.assertEqual(child2.parent, parent)
        self.assertEqual(parent.children, [child1, child2])

    def test_add_child(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent", children=[child1])
        parent.add_child(child2)
        self.assertEqual(child1.parent, parent)
        self.assertEqual(child2.parent, parent)
        self.assertEqual(parent.children, [child1, child2])

    def test_remove_child(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        parent = toga.Group("parent", children=[child1, child2])
        parent.remove_child(child1)
        self.assertEqual(child1.parent, None)
        self.assertEqual(child2.parent, parent)
        self.assertEqual(parent.children, [child2])

    def test_add_child_twice_in_constructor(self):
        child = toga.Group("child")
        parent = toga.Group("parent", children=[child, child])
        self.assertEqual(child.parent, parent)
        self.assertEqual(parent.children, [child])

    def test_change_children_after_initialize(self):
        child1 = toga.Group("child1")
        child2 = toga.Group("child2")
        child3 = toga.Group("child3")
        parent = toga.Group("parent", children=[child1, child2])
        parent.children = [child2, child3]
        self.assertEqual(child1.parent, None)
        self.assertEqual(child2.parent, parent)
        self.assertEqual(child3.parent, parent)
        self.assertEqual(parent.children, [child2, child3])

    def test_change_parent(self):
        child = toga.Group("child")
        parent1 = toga.Group("parent1", children=[child])
        parent2 = toga.Group("parent2")
        child.parent = parent2
        self.assertEqual(parent1.parent, None)
        self.assertEqual(parent1.children, [])
        self.assertEqual(parent2.parent, None)
        self.assertEqual(parent2.children, [child])
        self.assertEqual(child.parent, parent2)
        self.assertEqual(child.children, [])

    def test_groups_inheritance(self):
        top = toga.Group("C")
        middle = toga.Group("B", parent=top)
        bottom = toga.Group("A", parent=middle)
        groups = [top, middle, bottom]
        for i in range(0, 2):
            for j in range(i + 1, 3):
                self.assertTrue(groups[i].is_parent_of(groups[j]))
                self.assertTrue(groups[j].is_child_of(groups[i]))

    def test_group_order(self):
        parent = toga.Group("P", 1)
        parent2 = toga.Group("O", 2)
        self.assert_order(toga.Group('A', 1), toga.Group('A', 2))
        self.assert_order(toga.Group('B', 1), toga.Group('A', 2))
        self.assert_order(toga.Group('A'), toga.Group('B'))
        self.assert_order(
            parent,
            toga.Group('C', parent=parent),
            toga.Group('D', parent=parent),
            toga.Group('A', parent=parent, section=2),
            parent2,
            toga.Group("B", parent=parent2),
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
            g = toga.Group("A", section=2)

    def assert_order(self, *groups):
        for i in range(0, len(groups) - 1):
            for j in range(i + 1, len(groups)):
                self.assertLess(groups[i], groups[j])
                self.assertGreater(groups[j], groups[i])
                self.assertFalse(groups[j] < groups[i])
                self.assertFalse(groups[i] > groups[j])

