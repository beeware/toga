from toga_winforms.libs import Color, Size, WinForms

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
            # Workaround for loading image from url
            if self.interface._image._impl.url:
                self.native.Load(self.interface._image._impl.url)
            else:
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
            self.native.BackColor = Color.White

    def rehint(self):
        pass
