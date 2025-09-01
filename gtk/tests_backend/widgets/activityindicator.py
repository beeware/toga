from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = Gtk.Spinner

    def assert_spinner_is_hidden(self, value):
        # GTK automatically hides the widget on stop.
        assert (
            (not self.native.get_property("active")) or (not self.native.get_visible())
        ) == value
