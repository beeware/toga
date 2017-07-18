import unittest
from unittest.mock import MagicMock, Mock
import toga
import toga_dummy


class TestCoreSplitContainer(unittest.TestCase):
    def setUp(self):
        self.factory = MagicMock()
        self.factory.SplitContainer = MagicMock(return_value=MagicMock(spec=toga_dummy.factory.SplitContainer))
        self.content = [Mock(), Mock()]
        self.split = toga.SplitContainer(factory=self.factory)

    def test_factory_called(self):
        self.factory.SplitContainer.assert_called_with(interface=self.split)

    def test_setting_content_valid_input(self):
        new_content = [Mock(), Mock()]
        self.split.content = new_content
        self.assertEqual(self.split.content, new_content)

    def test_setting_content_false_input(self):
        with self.assertRaises(Exception):
            self.split.content = Mock()

        with self.assertRaises(ValueError):
            self.split.content = [Mock()]

    def test_setting_content_invokes_impl_method(self):
        new_content = [Mock(), Mock()]
        self.split.content = new_content
        self.split._impl.add_content.assert_any_call(0, new_content[0])
        self.split._impl.add_content.assert_any_call(1, new_content[1])

    @unittest.skip('FIXME: Not working at the moment')
    def test_setting_content_updates_app_and_window_on_new_content(self):
        new_content = [Mock(), Mock()]
        self.split.content = new_content
        new_content[0].app.assert_called_once_with(self.split.app)

    def test_direction_property_default(self):
        self.assertEqual(self.split.direction, True)

    def test_setting_direction_property_invokes_impl_method(self):
        new_value = False
        self.split.direction = new_value
        self.split._impl.set_direction.assert_called_with(new_value)
