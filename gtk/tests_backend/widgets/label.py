from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import to_toga_x_text_align, to_toga_y_text_align


class LabelProbe(SimpleProbe):
    native_class = Gtk.Label

    @property
    def text(self):
        return self.native.get_label()

    @property
    def text_align(self):
        return to_toga_x_text_align(self.native.get_xalign(), self.native.get_justify())

    @property
    def vertical_text_align(self):
        return

    def assert_vertical_text_align(self, expected):
        assert to_toga_y_text_align(self.native.get_yalign()) == expected
