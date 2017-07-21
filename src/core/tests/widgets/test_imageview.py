import unittest
from unittest.mock import MagicMock
import toga
import toga_dummy


class TestCoreImageView(unittest.TestCase):
    def setUp(self):
        # mock factory to return a mock button
        self.factory = MagicMock()
        self.factory.ImageView = MagicMock(return_value=MagicMock(spec=toga_dummy.widgets.imageview.ImageView))

        self.image_view = toga.ImageView(factory=self.factory)

    def test_factory_called(self):
        self.factory.ImageView.assert_called_once_with(interface=self.image_view)

    def test_setting_image_invokes_impl_method(self):
        new_image = 'not a image'
        self.image_view.image = new_image
        self.assertEqual(self.image_view._image, new_image)
        self.image_view._impl.set_image.assert_called_with(new_image)

    def test_getting_image_invokes_impl_method(self):
        image = self.image_view.image
        self.image_view._impl.get_image.assert_called_with()