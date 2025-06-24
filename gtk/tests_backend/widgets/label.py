import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe
from .properties import toga_x_text_align, toga_y_text_align


class LabelProbe(SimpleProbe):
    if GTK_VERSION >= (4, 0, 0):
        pytest.xfail("Labels are not yet supported on GTK4")
    native_class = Gtk.Label

    @property
    def text(self):
        return self.native.get_label()

    @property
    def text_align(self):
        return toga_x_text_align(self.native.get_xalign(), self.native.get_justify())

    @property
    def vertical_text_align(self):
        return

    def assert_vertical_text_align(self, expected):
        assert toga_y_text_align(self.native.get_yalign()) == expected
