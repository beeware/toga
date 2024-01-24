from travertino.size import at_least

from toga.colors import TRANSPARENT

from ..libs import Gtk
from .base import Widget


class Button(Widget):
    def create(self):
        self.native = Gtk.Button
        self.native.connect("clicked", self.gtk_clicked)

        self._icon = None

    def get_text(self):
        return self.native.get_label()

    def set_text(self, text):
        self.native.set_label(text)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            self.native.set_image(Gtk.Image.new_from_pixbuf(icon._impl.native_32))
            self.native.set_always_show_image(True)
        else:
            self.native.set_image(None)
            self.native.set_always_show_image(False)

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
        min_size, size = self.native.get_preferred_size()

        self.interface.intrinsic.width = at_least(min_size.width)
        self.interface.intrinsic.height = size.height

    def gtk_clicked(self, event):
        self.interface.on_press()
