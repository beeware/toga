from pytest import skip

from toga_gtk.libs import GdkPixbuf

from .probe import BaseProbe


class ImageProbe(BaseProbe):
    def __init__(self, app, image):
        super().__init__()
        self.app = app
        self.image = image
        assert isinstance(self.image._impl.native, GdkPixbuf.Pixbuf)

    def supports_extensions(self, extension):
        skip("GTK doesn't support saving images")
