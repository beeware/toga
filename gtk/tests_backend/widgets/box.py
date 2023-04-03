from toga_gtk.libs import Gtk

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = Gtk.Box

    @property
    def enabled(self):
        # A box is always enabled.
        return True
