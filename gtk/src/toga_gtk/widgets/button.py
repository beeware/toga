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
        text = self.native.get_label()
        return text if text else ""

    def set_text(self, text):
        if not isinstance(self.native.get_child(), Gtk.Image) or text != "":
            self.native.set_label(text)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            icon._impl.native.set_icon_size(Gtk.IconSize.LARGE)
            self.native.set_child(icon._impl.native)
        else:
            text = self.native.get_label()
            self.native.set_child(None)
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
        min_size, size = self.native.get_preferred_size()

        self.interface.intrinsic.width = at_least(min_size.width)
        self.interface.intrinsic.height = size.height

    def gtk_clicked(self, event):
        self.interface.on_press()
