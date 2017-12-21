import unittest

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

    def test_adding_children(self):
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
