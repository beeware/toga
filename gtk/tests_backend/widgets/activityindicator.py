import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = Gtk.Spinner
