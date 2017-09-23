import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestScrollContainer(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.ScrollContainer = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.ScrollContainer))

        self.sc = toga.ScrollContainer(factory=self.factory)

    def test_factory_is_called(self):
        self.factory.ScrollContainer.assert_called_once_with(interface=self.sc)

    def test_set_content_with_widget(self):
        self.assertEqual(self.sc.content, None, 'The default value of content should be None')

        new_content = MagicMock(toga.Box(factory=self.factory))
        self.sc.content = new_content
        self.assertEqual(self.sc.content, new_content)
        self.assertEqual(self.sc._content, new_content)
        self.sc._impl.set_content.assert_called_once_with(new_content._impl)

    def test_set_content_with_None(self):
        new_content = None
        self.assertEqual(self.sc.content, new_content)
        self.assertEqual(self.sc._content, new_content)
        self.sc._impl.set_content.assert_not_called()

    def test_vertical_property(self):
        self.assertEqual(self.sc.vertical, True, 'The default should be True')

        new_value = False
        self.sc.vertical = new_value
        self.assertEqual(self.sc.vertical, new_value)
        self.sc._impl.set_vertical.assert_called_with(new_value)

    def test_horizontal_property(self):
        self.assertEqual(self.sc.horizontal, True, 'The default should be True')

        new_value = False
        self.sc.horizontal = new_value
        self.assertEqual(self.sc.horizontal, new_value)
        self.sc._impl.set_horizontal.assert_called_with(new_value)
