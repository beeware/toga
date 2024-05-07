import pytest

from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = Gtk.Button

    @property
    def text(self):
        return self.native.get_label()

    def assert_no_icon(self):
        assert self.native.get_image() is None

    def assert_icon_size(self):
        icon = self.native.get_image().get_pixbuf()
        if icon:
            assert (icon.get_width(), icon.get_height()) == (32, 32)
        else:
            pytest.fail("Icon does not exist")

    async def press(self):
        self.native.clicked()
