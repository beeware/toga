import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestImage(unittest.TestCase):
    def setUp(self):
        # mock factory to return a mock button
        self.factory = MagicMock()
        self.factory.Image = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.image.Image))

        self.path = 'path/to/image.jpg'
        self.image = toga.Image(path=self.path,
                                factory=self.factory)

    def test_factory_called(self):
        self.factory.Image.assert_called_once_with(interface=self.image)

    def test_setting_path_invokes_impl_method(self):
        self.image._impl.load_image.assert_called_once_with(self.path)
