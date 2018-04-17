from toga_winforms.libs import *

from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = WinForms.PictureBox()
        self.native.interface = self.interface
        self.native.SizeMode = WinForms.PictureBoxSizeMode.CenterImage

    def get_image(self):
        return self.native.image

    def set_image(self, image):
        if image:
            # Workaround for loading image from url
            if isinstance(image._impl.native, str):
                self.native.Load(image._impl.native)
            else:
                self.native.Image = image._impl.native
        else:
            width = 0
            height = 0
            if self.interface.style.width:
                width = self.interface.style.width
            if self.interface.style.height:
                height = self.interface.style.height
            self.native.Image = Bitmap(Size(width, height))

    def rehint(self):
        pass
