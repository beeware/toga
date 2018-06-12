import toga
from toga.style import Pack
import toga_dummy
from toga_dummy.utils import TestCase


class WidgetTests(TestCase):
    def setUp(self):
        super().setUp()

        self.id = 'widget_id'
        self.style = Pack(padding=666)

        self.widget = toga.Widget(id=self.id,
                                  style=self.style,
                                  factory=toga_dummy.factory)

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
        """
        """
        self.assertEqual(self.widget.children, [], 'No child was added, should return a empty list.')
        # Create a child widget to add to the our widget.
        child = toga.Widget(factory=toga_dummy.factory)

        with self.assertRaises(ValueError, msg='Widget cannot have children.'):
            self.widget.add(child)

        # Deliberately set widget._children = [] to allow it to have children.
        # Only for test purposes!
        self.widget._children = []
        self.widget.add(child)
        self.assertEqual(self.widget.children, [child])

    def test_adding_children(self):
        self.assertEqual(self.widget.children, [], ' No children added, should return a empty list.')
        # Create 2 children to add to widget.
        child1 = toga.Widget(factory=toga_dummy.factory)
        child2 = toga.Widget(factory=toga_dummy.factory)

        self.widget._children = []
        self.widget.add(child1, child2)
        self.assertEqual(self.widget.children, [child1, child2])
