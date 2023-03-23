from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = Gtk.Spinner

    @property
    def is_running(self):
        return self.native.get_property("active")
