from travertino.size import at_least

from toga.colors import TRANSPARENT

from ..libs import Gtk
from .base import Widget


class Button(Widget):
    def create(self):
        self.native = Gtk.Button()
        self.native.set_name(f"toga-{self.interface.id}")
        self.native.get_style_context().add_class("toga")
        self.native.interface = self.interface

        self.native.connect("show", lambda event: self.rehint())
        self.native.connect("clicked", self.gtk_on_press)

    def get_text(self):
        return self.native.get_label()

    def set_text(self, text):
        self.native.set_label(text)
        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    def set_on_press(self, handler):
        # No special handling required
        pass

    def set_background_color(self, color):
        # Buttons interpret TRANSPARENT backgrounds as a reset
        if color == TRANSPARENT:
            color = None
        super().set_background_color(color)

    def gtk_rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]

    def gtk_on_press(self, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)
