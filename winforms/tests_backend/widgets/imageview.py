import System.Windows.Forms as WinForms

from toga.colors import TRANSPARENT

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = WinForms.PictureBox

    @property
    def preserve_aspect_ratio(self):
        return self.native.SizeMode == WinForms.PictureBoxSizeMode.Zoom

    def assert_image_size(self, width, height):
        # Winforms internally scales the image to the container,
        # so there's no image size check required.
        pass

    def assert_background_color(self, color):
        if color is None:
            super().assert_background_color(TRANSPARENT)
        else:
            super().assert_background_color(color)
