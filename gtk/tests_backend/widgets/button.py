import pytest

from toga.colors import TRANSPARENT
from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = Gtk.Button

    @property
    def text(self):
        text = self.native.get_label()
        return text if text else ""

    def assert_no_icon(self):
        assert not isinstance(self.native.get_child(), Gtk.Image)

    def assert_icon_size(self):
        icon = self.native.get_child()
        if isinstance(icon, Gtk.Image):
            assert (icon.get_width(), icon.get_height()) == (32, 32)
        else:
            pytest.fail("Icon does not exist")

    @property
    def background_color(self):
        color = super().background_color
        # Background color of TRANSPARENT is treated as a reset.
        if color == TRANSPARENT:
            return None
        return color

    async def press(self):
        self.native.emit("clicked")
