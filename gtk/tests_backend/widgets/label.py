from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import toga_xalignment, toga_yalignment


class LabelProbe(SimpleProbe):
    native_class = Gtk.Label

    @property
    def text(self):
        return self.native.get_label()

    @property
    def alignment(self):
        return toga_xalignment(self.native.get_xalign(), self.native.get_justify())

    @property
    def vertical_alignment(self):
        return

    def assert_vertical_alignment(self, expected):
        assert toga_yalignment(self.native.get_yalign()) == expected
