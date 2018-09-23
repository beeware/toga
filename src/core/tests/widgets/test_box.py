from unittest.mock import patch

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class BoxTests(TestCase):
    def setUp(self):
        super().setUp()
        self.children = [toga.Widget(factory=toga_dummy.factory)]
        self.box = toga.Box(children=self.children, factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.box._impl.interface, self.box)
        self.assertActionPerformed(self.box, 'create Box')

    @patch('toga.widgets.base.get_platform_factory')
    def test_box_with_without_factory(self, mock_function):
        btn = toga.Box()
        mock_function.assert_called_once_with(None)

    def test_children_added(self):
        self.assertEqual(self.box._children, self.children)
