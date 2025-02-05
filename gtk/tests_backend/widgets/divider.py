import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = Gtk.Separator

    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("GTK4 doesn't support a divider yet")
