from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = Gtk.Spinner
