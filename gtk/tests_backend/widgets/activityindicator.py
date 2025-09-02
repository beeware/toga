from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = Gtk.Spinner

    def assert_spinner_is_hidden(self, value):
        # GTK automatically hides the widget on stop.
        is_visible = self.native.get_property("active") and self.native.get_visible()
        assert is_visible == (not value)
