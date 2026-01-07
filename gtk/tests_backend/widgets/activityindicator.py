from toga_gtk.libs import ADW_VERSION, GTK_VERSION, Adw, Gtk

from .base import SimpleProbe

if Adw is not None and ADW_VERSION >= (1, 6, 0):

    class ActivityIndicatorProbe(SimpleProbe):
        native_class = Adw.Spinner

        def assert_spinner_is_hidden(self, value):
            assert self.native.get_visible() == (not value)

else:

    class ActivityIndicatorProbe(SimpleProbe):
        native_class = Gtk.Spinner

        def assert_spinner_is_hidden(self, value):
            # GTK automatically hides the widget on stop.
            if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
                is_visible = (
                    self.native.get_property("active") and self.native.get_visible()
                )
            else:  # pragma: no-cover-if-gtk3
                is_visible = (
                    self.native.get_property("spinning") and self.native.get_visible()
                )
            assert is_visible == (not value)
