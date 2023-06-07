from toga.widgets.imageview import rehint_imageview
from toga_winforms.libs import Size, WinForms

from .base import Widget


class ImageView(Widget):
    def create(self):
        self.native = WinForms.PictureBox()
        self.native.interface = self.interface
        self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom

    def set_image(self, image):
        # If an image already exists, ensure it is destroyed
        if self.native.Image is not None:
            self.native.Image.Dispose()

        if image:
            self.native.Image = self.interface._image._impl.native
        else:
            width = 0
            height = 0
            if self.interface.style.width:
                width = self.interface.style.width
            if self.interface.style.height:
                height = self.interface.style.height

            self.native.Size = Size(width, height)
            # Setting background color to white is not necessary, but it shows the
            # picture frame
            # self.native.BackColor = Color.White

    def rehint(self):
        width, height, preserve_aspect_ratio = rehint_imageview(
            image=self.interface.image,
            style=self.interface.style,
        )
        self.interface.intrinsic.width = width
        self.interface.intrinsic.height = height
        if preserve_aspect_ratio:
            self.native.SizeMode = WinForms.PictureBoxSizeMode.Zoom
        else:
            self.native.SizeMode = WinForms.PictureBoxSizeMode.StretchImage
