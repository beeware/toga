from pathlib import Path

import toga
from toga_dummy.utils import TestCase


class ImageTests(TestCase):
    def setUp(self):
        super().setUp()

        # an App must have been created before creating images because paths
        # can be relative to the app path.
        self.app = toga.App(
            formal_name="Image Test App",
            app_id="org.beeware.test_image",
        )

    def test_path_file_non_existent_image(self):
        # Creating an image from a path that doesn't exist raises an error.
        try:
            toga.Image(path=Path("does/not/exist/image.jpg"))
            self.fail("The image does not exist")  # pragma: nocover
        except FileNotFoundError:
            pass

    def test_path_file_image(self):
        # Creating an image from a path.
        image = toga.Image(path=Path(toga.__file__).parent / "resources" / "toga.png")

        self.assertIsNotNone(image._impl)
        self.assertEqual(
            image._impl.interface.path,
            Path(toga.__file__).parent / "resources" / "toga.png",
        )

    def test_str_file_non_existent_image(self):
        # Creating an image from a string path that doesn't exist raises an error.
        try:
            toga.Image(path="does/not/exist/image.jpg")
            self.fail("The image does not exist")  # pragma: nocover
        except FileNotFoundError:
            pass

    def test_str_file_image(self):
        # Creating an image from a string path.
        image = toga.Image(path=f"{Path(toga.__file__).parent}/resources/toga.png")

        self.assertIsNotNone(image._impl)
        self.assertEqual(
            image._impl.interface.path,
            Path(toga.__file__).parent / "resources" / "toga.png",
        )

    def test_url_image(self):
        # Creating an image from a URL.
        url_image = toga.Image(path="https://example.com/image.png")

        self.assertEqual(
            url_image._impl.interface.path, "https://example.com/image.png"
        )
        self.assertActionPerformedWith(
            url_image, "load image url", url="https://example.com/image.png"
        )

    def test_bytes_image(self):
        data = bytes([1])
        bytes_image = toga.Image(data=data)

        self.assertEqual(bytes_image._impl.interface, bytes_image)
        self.assertActionPerformedWith(bytes_image, "load image data", data=data)

    def test_not_enough_arguments(self):
        with self.assertRaises(ValueError):
            toga.Image(None)

    def test_too_many_arguments(self):
        path = "/image.png"
        data = bytes([1])
        with self.assertRaises(ValueError):
            toga.Image(path=path, data=data)

    def test_bind(self):
        # Bind is a deprecated no-op
        image = toga.Image(path=Path(toga.__file__).parent / "resources" / "toga.png")

        with self.assertWarns(DeprecationWarning):
            bound = image.bind()

        self.assertIsNotNone(image._impl)
        self.assertEqual(
            image._impl.interface.path,
            Path(toga.__file__).parent / "resources" / "toga.png",
        )

        # The bound image is the _impl.
        self.assertEqual(bound, image._impl)

    def test_image_save(self):
        save_path = Path("/path/to/save.png")
        image = toga.Image(path=Path(toga.__file__).parent / "resources" / "toga.png")
        image.save(save_path)
        self.assertActionPerformedWith(image, "save", path=save_path)
