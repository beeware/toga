import toga
from toga_gtk.libs import Gtk

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = Gtk.Separator

    @property
    def direction(self):
        return (
            toga.Divider.VERTICAL
            if self.native.get_orientation() == Gtk.Orientation.VERTICAL
            else toga.Divider.HORIZONTAL
        )
