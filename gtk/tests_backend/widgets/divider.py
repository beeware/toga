from toga_gtk.libs import Gtk

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = Gtk.Separator

    @property
    def enabled(self):
        # A Divider is always enabled.
        return True
