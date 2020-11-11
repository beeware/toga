import toga
import toga_dummy
from toga.style import Pack
from toga_dummy.utils import TestCase


class WidgetTests(TestCase):
    def setUp(self):
        super().setUp()

        self.id = 'widget_id'
        self.style = Pack(padding=666)

        self.widget = toga.Widget(
            id=self.id,
            style=self.style,
            factory=toga_dummy.factory
        )

    def test_arguments_were_set_correctly(self):
        self.assertEqual(self.widget.id, self.id)
        self.assertEqual(self.widget.style.padding, self.style.padding)

    def test_create_widget_with_no_style(self):
        widget = toga.Widget(factory=toga_dummy.factory)
        self.assertTrue(isinstance(widget.style, Pack))

    def test_enabled_with_None(self):
        # Using a Box for test because we need a concrete implementation to use this property.
        box = toga.Box(factory=toga_dummy.factory)
        box.enabled = None
        self.assertFalse(box.enabled)
        self.assertActionPerformedWith(box, 'set enabled', value=None)

    def test_adding_child(self):
        self.assertEqual(self.widget.children, [], 'No child was added, should return an empty list.')
        # Create a child widget to add to widget.
        child = toga.Widget(factory=toga_dummy.factory)

        with self.assertRaises(ValueError, msg='Widget cannot have children.'):
            self.widget.add(child)

        # Deliberately set widget._children = [] to allow it to have children.
        # Only for test purposes!
        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])

    def test_adding_children(self):
        self.assertEqual(self.widget.children, [], 'No children added, should return an empty list.')
        # Create 2 children to add to widget.
        child1 = toga.Widget(factory=toga_dummy.factory)
        child2 = toga.Widget(factory=toga_dummy.factory)

        self.widget._children = []
        self.widget.add(child1, child2)
        self.assertEqual(self.widget.children, [child1, child2])

    def test_adding_child_with_existing_parent(self):
        # Create a second parent widget.
        widget2 = toga.Widget(factory=toga_dummy.factory)
        # Create a child widget to add to widget2 before adding to widget.
        child = toga.Widget(factory=toga_dummy.factory)

        widget2._children = []
        widget2.add(child)
        self.assertEqual(widget2.children, [child])

        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(widget2.children, [])

    def test_inserting_child_into_empty_list(self):
        self.assertEqual(self.widget.children, [], 'No child was inserted, should return an empty list.')
        # Create a child widget to insert into widget.
        child = toga.Widget(factory=toga_dummy.factory)

        with self.assertRaises(ValueError, msg='Widget cannot have children.'):
            self.widget.insert(0, child)

        self.widget._children = []
        self.widget.insert(0, child)
        self.assertEqual(self.widget.children, [child])

    def test_inserting_child_into_list_containing_one_child(self):
        self.assertEqual(self.widget.children, [], 'No child was inserted, should return an empty list.')
        # Create 2 children to insert into widget.
        child1 = toga.Widget(factory=toga_dummy.factory)
        child2 = toga.Widget(factory=toga_dummy.factory)

        self.widget._children = []
        self.widget.insert(0, child1)
        self.widget.insert(1, child2)
        self.assertEqual(self.widget.children, [child1, child2])

    def test_inserting_child_into_list_containing_three_children(self):
        self.assertEqual(self.widget.children, [], 'No child was inserted, should return an empty list.')
        # Create 3 children to add to widget.
        child1 = toga.Widget(factory=toga_dummy.factory)
        child2 = toga.Widget(factory=toga_dummy.factory)
        child3 = toga.Widget(factory=toga_dummy.factory)
        # Create a child to insert into widget.
        child4 = toga.Widget(factory=toga_dummy.factory)

        self.widget._children = []
        self.widget.add(child1, child2, child3)
        self.widget.insert(2, child4)

        self.assertEqual(self.widget.children, [child1, child2, child4, child3])

    def test_inserting_child_with_existing_parent(self):
        # Create a second parent widget.
        widget2 = toga.Widget(factory=toga_dummy.factory)
        # Create a child widget to insert into widget2 before inserting into widget.
        child = toga.Widget(factory=toga_dummy.factory)

        widget2._children = []
        widget2.insert(0, child)
        self.assertEqual(widget2.children, [child])

        self.widget._children = []
        self.widget.insert(0, child)
        self.assertEqual(self.widget.children, [child])
        self.assertEqual(widget2.children, [])

    def test_removing_child(self):
        self.assertEqual(self.widget.children, [], 'No child was added, should return an empty list.')
        # Create a child widget to add then remove from widget.
        child = toga.Widget(factory=toga_dummy.factory)

        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])

        self.widget.remove(child)
        self.assertEqual(self.widget.children, [])

    def test_removing_children(self):
        self.assertEqual(self.widget.children, [], 'No children added, should return an empty list.')
        # Create 2 children to add then remove from widget.
        child1 = toga.Widget(factory=toga_dummy.factory)
        child2 = toga.Widget(factory=toga_dummy.factory)

        self.widget._children = []
        self.widget.add(child1, child2)
        self.assertEqual(self.widget.children, [child1, child2])

        self.widget.remove(child1, child2)
        self.assertEqual(self.widget.children, [])

    def test_removing_two_out_of_three_children(self):
        self.assertEqual(self.widget.children, [], 'No children added, should return am empty list.')
        # Create 3 children to add to widget, 2 of which will be removed.
        child1 = toga.Widget(factory=toga_dummy.factory)
        child2 = toga.Widget(factory=toga_dummy.factory)
        child3 = toga.Widget(factory=toga_dummy.factory)

        self.widget._children = []
        self.widget.add(child1, child2, child3)
        self.assertEqual(self.widget.children, [child1, child2, child3])

        self.widget.remove(child1, child3)
        self.assertEqual(self.widget.children, [child2])
