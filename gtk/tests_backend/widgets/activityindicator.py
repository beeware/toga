import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("ActivityIndicator is not yet supported with GTK4")
    native_class = Gtk.Spinner
