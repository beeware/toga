import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("Box is not yet supported with GTK4")
    native_class = Gtk.Box
