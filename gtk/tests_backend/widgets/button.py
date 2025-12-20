import pytest

from toga.colors import TRANSPARENT
from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = Gtk.Button

    @property
    def text(self):
        label = self.native.get_label()
        return label if label else ""

    def assert_no_icon(self):
        if GTK_VERSION < (4, 0, 0):
            assert self.native.get_image() is None
        else:
            assert isinstance(self.native.get_child(), Gtk.Label)

    def assert_icon_size(self):
        if GTK_VERSION < (4, 0, 0):
            icon = self.native.get_image().get_pixbuf()
            if icon:
                assert (icon.get_width(), icon.get_height()) == (32, 32)
            else:
                pytest.fail("Icon does not exist")
        else:
            assert isinstance(self.native.get_child(), Gtk.Image)
            assert self.native.get_child().get_icon_size() == Gtk.IconSize.LARGE

    @property
    def background_color(self):
        color = super().background_color
        # Background color of TRANSPARENT is treated as a reset.
        if color == TRANSPARENT:
            return None
        return color

    async def press(self):
        if GTK_VERSION < (4, 0, 0):
            self.native.clicked()
        else:
            self.native.emit("clicked")
