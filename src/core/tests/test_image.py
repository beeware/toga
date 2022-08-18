from pathlib import Path

import toga
import toga_dummy
from toga_dummy.utils import TestCase


class ImageTests(TestCase):
    def setUp(self):
        super().setUp()

        # an App must have been created before calling image.bind
        # because it tries to resolve the image path against the app path.
        toga.App(formal_name='Image Test App',
                 app_id='org.beeware.test_image',
                 factory=toga_dummy.factory)
        self.file_path = Path('path/to/image.jpg')
        self.url_path = 'http://website.com/image.jpg'
        self.path_file_image = toga.Image(path=self.file_path)
        self.str_file_image = toga.Image(path=str(self.file_path))
        self.url_image = toga.Image(path=self.url_path)

    def test_path_file_image_binding(self):
        # Image is initially unbound
        self.assertIsNone(self.path_file_image._impl)

        # Bind the image; the file doesn't exist, so it raises an error.
        try:
            self.path_file_image.bind(factory=toga_dummy.factory)
            self.fail('The image should not bind')  # pragma: nocover
        except FileNotFoundError:
            pass

        # Image remains unbound
        self.assertIsNone(self.path_file_image._impl)

    def test_str_file_image_binding(self):
        # Image is initially unbound
        self.assertIsNone(self.str_file_image._impl)

        # Bind the image; the file doesn't exist, so it raises an error.
        try:
            self.str_file_image.bind(factory=toga_dummy.factory)
            self.fail('The image should not bind')  # pragma: nocover
        except FileNotFoundError:
            pass

        # Image remains unbound
        self.assertIsNone(self.str_file_image._impl)

    def test_url_image_binding(self):
        # Image is initially unbound
        self.assertIsNone(self.url_image._impl)

        # Bind the image
        self.url_image.bind(factory=toga_dummy.factory)

        # Image is bound correctly
        self.assertEqual(self.url_image._impl.interface, self.url_image)
        self.assertActionPerformedWith(self.url_image, 'load image url', url=self.url_path)

    def test_path_file_image_path(self):
        self.assertEqual(self.path_file_image.path, self.file_path)

    def test_str_file_image_path(self):
        self.assertEqual(self.str_file_image.path, self.file_path)

    def test_url_image_path(self):
        self.assertEqual(self.url_image.path, self.url_path)
