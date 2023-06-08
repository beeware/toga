from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ImageViewProbe(SimpleProbe):
    native_class = Gtk.Image

    @property
    def preserve_aspect_ratio(self):
        return self.impl._aspect_ratio is not None
