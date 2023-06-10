from travertino.size import at_least

from toga.colors import TRANSPARENT

from ..libs import Gtk
from .base import Widget


class Button(Widget):
    def create(self):
        self.native = Gtk.Button()
        self.native.connect("clicked", self.gtk_clicked)

    def get_text(self):
        return self.native.get_label()

    def set_text(self, text):
        self.native.set_label(text)

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    def set_background_color(self, color):
        # Buttons interpret TRANSPARENT backgrounds as a reset
        if color == TRANSPARENT:
            color = None
        super().set_background_color(color)

    def rehint(self):
        # print(
        #     "REHINT",
        #     self,
        #     self.native.get_preferred_size()[0].width,
        #     self.native.get_preferred_size()[0].height,
        # )
        min_size, natural_size = self.native.get_preferred_size()

        self.interface.intrinsic.width = at_least(min_size.width)
        self.interface.intrinsic.height = natural_size.height

    def gtk_clicked(self, event):
        self.interface.on_press(None)
