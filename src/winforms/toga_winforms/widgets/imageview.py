from toga_winforms.libs import WinForms, Color, Size

from .base import Widget


class ImageView(Widget):

    def create(self):
        self.native = WinForms.PictureBox()
        self.native.interface = self.interface
        self.native.SizeMode = WinForms.PictureBoxSizeMode.StretchImage

    def get_image(self):
        return self.native.Image

    def set_image(self, image):
        if image and image.path is not None:
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

            self.native.Size = Size(width, height)
            # Setting background color to white is not necessary, but it shows the
            # picture frame
            self.native.BackColor = Color.White

    def rehint(self):
        pass
