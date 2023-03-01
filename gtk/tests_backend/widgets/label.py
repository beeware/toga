from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import toga_alignment


class LabelProbe(SimpleProbe):
    native_class = Gtk.Label

    @property
    def text(self):
        return self.native.get_label()

    @property
    def alignment(self):
        return toga_alignment(
            self.native.get_xalign(),
            self.native.get_yalign(),
            self.native.get_justify(),
        )
