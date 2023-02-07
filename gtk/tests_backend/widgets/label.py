from pytest import skip

from toga_gtk.libs import Gtk

from .base import SimpleProbe


class LabelProbe(SimpleProbe):
    native_class = Gtk.Label

    @property
    def text(self):
        return self.native.get_label()

    @property
    def alignment(self):
        skip("alignment probe not implemented")
