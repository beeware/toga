from toga_gtk.libs import Gtk

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = Gtk.Box
