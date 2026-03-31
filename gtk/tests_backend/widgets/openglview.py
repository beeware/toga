from toga_gtk.libs import Gtk

from .base import SimpleProbe


class OpenGLViewProbe(SimpleProbe):
    native_class = Gtk.GLArea
    buttons = frozenset()
