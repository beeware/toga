from pytest import skip

from toga_gtk.libs import Gtk

from .base import SimpleProbe


class LabelProbe(SimpleProbe):
    native_class = Gtk.Label

    @property
    def text(self):
        return self.native.get_label()

    @property
    def color(self):
        skip("color probe not implemented")

    @property
    def background_color(self):
        skip("background color probe not implemented")

    @property
    def font(self):
        skip("font probe not implemented")

    @property
    def alignment(self):
        skip("alignment probe not implemented")
