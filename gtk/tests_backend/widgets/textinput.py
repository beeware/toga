from toga_gtk.libs import Gtk

from .base import SimpleProbe


class TextInputProbe(SimpleProbe):
    native_class = Gtk.Entry
