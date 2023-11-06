from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = Gtk.Image

    @property
    def preserve_aspect_ratio(self):
        return self.impl._aspect_ratio is not None

    def assert_image_size(self, width, height):
        # Confirm the underlying pixelbuf has been scaled to the appropriate size.
        pixbuf = self.native.get_pixbuf()
        assert (pixbuf.get_width(), pixbuf.get_height()) == (width, height)
