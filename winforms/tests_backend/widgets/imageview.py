from toga_winforms.libs import WinForms

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = WinForms.PictureBox

    @property
    def preserve_aspect_ratio(self):
        return self.native.SizeMode == WinForms.PictureBoxSizeMode.Zoom
