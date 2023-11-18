from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from System.Drawing import Bitmap

from toga.widgets.imageview import rehint_imageview

from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = WinForms.PictureBox()
        self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom

        # If self.native.Image is None, Winforms renders it as a white square
        # with a red cross through it. Ensure we always have an actual image,
        # using a 1x1 blank bitmap for the None case.
        self.native.Image = self._empty_image()

    def _empty_image(self):
        return Bitmap(1, 1)

    def set_image(self, image):
        # Destroy the existing image.
        self.native.Image.Dispose()

        if image:
            self.native.Image = self.interface._image._impl.native
        else:
            self.native.Image = self._empty_image()

    def rehint(self):
        width, height, aspect_ratio = rehint_imageview(
            self.interface.image, self.interface.style, self.dpi_scale
        )
        self.interface.intrinsic.width = self.scale_out(width, ROUND_UP)
        self.interface.intrinsic.height = self.scale_out(height, ROUND_UP)
        if aspect_ratio is not None:
            self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom
        else:
            self.native.SizeMode = WinForms.PictureBoxSizeMode.StretchImage
