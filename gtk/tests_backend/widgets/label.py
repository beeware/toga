from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import toga_x_text_alignment, toga_y_text_alignment


class LabelProbe(SimpleProbe):
    native_class = Gtk.Label

    @property
    def text(self):
        return self.native.get_label()

    @property
    def text_alignment(self):
        return toga_x_text_alignment(
            self.native.get_xalign(), self.native.get_justify()
        )

    @property
    def vertical_text_alignment(self):
        return

    def assert_vertical_text_alignment(self, expected):
        assert toga_y_text_alignment(self.native.get_yalign()) == expected
