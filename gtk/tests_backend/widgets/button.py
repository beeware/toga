from toga_gtk.libs import Gtk

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = Gtk.Button

    @property
    def text(self):
        return self.native.get_label()

    @property
    def background_color(self):
        color = super().background_color
        # Background color of
        if color.r == 0 and color.g == 0 and color.b == 0 and color.a == 0.0:
            return None
        return color

    def press(self):
        self.native.clicked()
