from toga.widgets.imageview import rehint_imageview
from toga_winforms.libs import Bitmap, WinForms

from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = WinForms.PictureBox()
        self.native.interface = self.interface
        self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom

        # If self.native.Image is None, Winforms renders it as a white square
        # with a red cross through it. Ensure we always have an actual image,
        # using a 1x1 blank bitmap for the None case.
        self.native.Image = self._empty_image()

    def _empty_image(self):
        return Bitmap(1, 1)

    def set_image(self, image):
        # If an image already exists, ensure it is destroyed
        if self.native.Image is not None:
            self.native.Image.Dispose()

        if image:
            self.native.Image = self.interface._image._impl.native
        else:
            self.native.Image = self._empty_image()

    def rehint(self):
        width, height, aspect_ratio = rehint_imageview(
            image=self.interface.image,
            style=self.interface.style,
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
        if aspect_ratio is not None:
            self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom
        else:
            self.native.SizeMode = WinForms.PictureBoxSizeMode.StretchImage
