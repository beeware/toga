import toga

import toga_dummy
from toga_dummy.utils import TestCase


class ImageTests(TestCase):
    def setUp(self):
        super().setUp()

        self.path = 'path/to/image.jpg'
        self.image = toga.Image(path=self.path)

    def test_object_created(self):
        # Image is initially unbound
        self.assertIsNone(self.image._impl)

        # Bind the image; the file doesn't exist, so it raises an error.
        try:
            self.image.bind(factory=toga_dummy.factory)
            self.fail('The image should not bind')
        except FileNotFoundError:
            pass

        # self.assertEqual(self.image._impl.interface, self.image)
        # self.assertActionPerformedWith(self.image, 'load image', path=self.path)

    def test_path(self):
        self.assertEqual(self.image.path, self.path)
