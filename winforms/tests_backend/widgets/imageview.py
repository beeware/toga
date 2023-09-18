import System.Windows.Forms as WinForms

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
