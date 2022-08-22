import unittest

import toga
from tests.utils import order_test

from tests.command.constants import PARENT_GROUP1, PARENT_GROUP2


class TestCommandsGroup(unittest.TestCase):

    def test_group_init_no_order(self):
        grp = toga.Group('text')
        self.assertEqual(grp.text, 'text')
        self.assertEqual(grp.order, 0)

    def test_group_init_with_order(self):
        grp = toga.Group('text', 2)
        self.assertEqual(grp.text, 'text')
        self.assertEqual(grp.order, 2)

    def test_hashable(self):
        grp1 = toga.Group('text 1')
        grp2 = toga.Group('text 2')

        # The hash is based on the full path, not just the text.
        # This allows texts to be non-unique, as long as they're in
        # different groups
        grp1_child = toga.Group('text', parent=grp1)
        grp2_child = toga.Group('text', parent=grp2)

        # Insert the groups as keys in a dict. This is
        # only possible if Group is hashable.
        groups = {
            grp1: 'First',
            grp2: 'Second',
            grp1_child: "Child of 1",
            grp2_child: "Child of 2",
        }

        self.assertEqual(groups[grp1], "First")
        self.assertEqual(groups[grp2], "Second")
        self.assertEqual(groups[grp1_child], "Child of 1")
        self.assertEqual(groups[grp2_child], "Child of 2")

    def test_group_eq(self):
        self.assertEqual(toga.Group('A'), toga.Group('A'))
        self.assertEqual(toga.Group('A', 1), toga.Group('A', 1))
        self.assertNotEqual(toga.Group('A'), toga.Group('B'))
        self.assertNotEqual(toga.Group('A'), None)
        self.assertNotEqual(toga.Group('A', 1), toga.Group('A', 2))
        self.assertNotEqual(toga.Group('A', 1), toga.Group('B', 1))

    def test_set_parent_in_constructor(self):
        parent = toga.Group("parent")
        child = toga.Group("child", parent=parent)
        self.assert_parent_and_root(parent, None, parent)
        self.assert_parent_and_root(child, parent, parent)

    def test_set_parent_in_property(self):
        parent = toga.Group("parent")
        child = toga.Group("child")
        child.parent = parent
        self.assert_parent_and_root(parent, None, parent)
        self.assert_parent_and_root(child, parent, parent)

    def test_change_parent(self):
        parent1 = toga.Group("parent1")
        parent2 = toga.Group("parent2")
        child = toga.Group("child", parent=parent1)
        child.parent = parent2
        self.assert_parent_and_root(parent1, None, parent1)
        self.assert_parent_and_root(parent2, None, parent2)
        self.assert_parent_and_root(child, parent2, parent2)

    def test_is_parent_and_is_child_of(self):
        top = toga.Group("C")
        middle = toga.Group("B", parent=top)
        bottom = toga.Group("A", parent=middle)
        groups = [top, middle, bottom]
        for i in range(0, 2):
            for j in range(i + 1, 3):
                self.assertTrue(groups[i].is_parent_of(groups[j]))
                self.assertTrue(groups[j].is_child_of(groups[i]))

    def test_is_parent_of_none(self):
        group = toga.Group("A")
        self.assertFalse(group.is_parent_of(None))

    def test_root(self):
        top = toga.Group("C")
        middle = toga.Group("B", parent=top)
        bottom = toga.Group("A", parent=middle)
        self.assertEqual(top.root, top)
        self.assertEqual(middle.root, top)
        self.assertEqual(top.root, top)
        self.assertEqual(bottom.root, top)

    test_order_by_number = order_test(toga.Group('A', 1), toga.Group('A', 2))
    test_order_ignore_text = order_test(toga.Group('B', 1), toga.Group('A', 2))
    test_order_by_text = order_test(toga.Group('A'), toga.Group('B'))
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
            repr(toga.Group("A")), "<Group text=A order=0 parent=None>"
        )
        self.assertEqual(
            repr(toga.Group("A", parent=parent)),
            "<Group text=A order=0 parent=P>"
        )

    def test_set_section_without_parent(self):
        with self.assertRaises(ValueError):
            toga.Group("A", section=2)

    def test_set_parent_causes_cyclic_parenting(self):
        parent = toga.Group("P")
        child = toga.Group("C", parent=parent)
        with self.assertRaises(ValueError):
            parent.parent = child
        self.assert_parent_and_root(parent, None, parent)
        self.assert_parent_and_root(child, parent, parent)

    def test_cannot_set_self_as_parent(self):
        group = toga.Group("P")
        with self.assertRaises(ValueError):
            group.parent = group
        self.assert_parent_and_root(group, None, group)

    def test_cannot_set_child_to_be_a_parent_of_its_grandparent(self):
        grandparent = toga.Group("G")
        parent = toga.Group("P", parent=grandparent)
        child = toga.Group("C", parent=parent)
        with self.assertRaises(ValueError):
            grandparent.parent = child
        self.assert_parent_and_root(grandparent, None, grandparent)
        self.assert_parent_and_root(parent, grandparent, grandparent)
        self.assert_parent_and_root(child, parent, grandparent)

    def assert_parent_and_root(self, group, parent, root):
        self.assertEqual(group.parent, parent)
        self.assertEqual(group.root, root)

    def test_missing_argument(self):
        "If the no text is provided for the group, an error is raised"
        # This test is only required as part of the backwards compatibility
        # path renaming label->text; when that shim is removed, this teset
        # validates default Python behavior
        with self.assertRaises(TypeError):
            toga.Group()

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################

    def test_label_deprecated(self):
        grp = toga.Group(label='text')
        new_text = 'New Text'
        with self.assertWarns(DeprecationWarning):
            grp.label = new_text
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(grp.label, new_text)
        self.assertEqual(grp.text, new_text)

    def test_init_with_deprecated(self):
        # label is a deprecated argument
        with self.assertWarns(DeprecationWarning):
            toga.Group(label='test')

        # can't specify both label *and* text
        with self.assertRaises(ValueError):
            toga.Group(
                label='test',
                text='test',
            )

    ######################################################################
    # End backwards compatibility.
    ######################################################################
