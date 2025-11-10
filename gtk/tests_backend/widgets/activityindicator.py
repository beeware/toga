import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("ActivityIndicator is not yet supported with GTK4")
    native_class = Gtk.Spinner

    def assert_spinner_is_hidden(self, value):
        # GTK automatically hides the widget on stop.
        is_visible = self.native.get_property("active") and self.native.get_visible()
        assert is_visible == (not value)
