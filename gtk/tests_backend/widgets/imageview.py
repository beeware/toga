from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = Gtk.Picture

    @property
    def preserve_aspect_ratio(self):
        return self.impl._aspect_ratio is not None

    def assert_image_size(self, width, height):
        # Confirm the underlying pixelbuf (Gtk.Picture's content) has been scaled
        # to the appropriate size.
        assert (
            self.native.get_paintable().get_width(),
            self.native.get_paintable().get_height(),
        ) == (width, height)
