import toga
import toga_dummy
from toga_dummy.utils import TestCase


class ImageViewTests(TestCase):
    def setUp(self):
        super().setUp()

        self.image_view = toga.ImageView(factory=toga_dummy.factory)

    def test_widget_created(self):
        self.assertEqual(self.image_view._impl.interface, self.image_view)
        self.assertActionPerformed(self.image_view, 'create ImageView')

    def test_setting_image_invokes_impl_method(self):
        new_image = 'not a image'
        self.image_view.image = new_image
        self.assertEqual(self.image_view._image, new_image)
        self.assertValueSet(self.image_view, 'image', new_image)

    def test_getting_image_invokes_impl_method(self):
        image = self.image_view.image
        self.assertValueGet(self.image_view, 'image')
