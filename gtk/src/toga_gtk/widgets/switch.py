from travertino.size import at_least

from ..libs import Gtk, get_color_css, get_font_css
from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = Gtk.Box()

        self.label = Gtk.Label(xalign=0)
        self.label.set_name(f"toga-{self.interface.id}-label")
        self.label.get_style_context().add_class("toga")
        self.label.set_line_wrap(True)

        self.switch = Gtk.Switch()
        self.switch.set_name(f"toga-{self.interface.id}-switch")
        self.switch.get_style_context().add_class("toga")
        self.switch.connect("notify::active", self.gtk_on_change)

        self.native.pack_start(self.label, True, True, 0)
        self.native.pack_start(self.switch, False, False, 0)
        self.native.connect("show", lambda event: self.refresh())

    def gtk_on_change(self, widget, state):
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    def set_on_change(self, handler):
        pass

    def get_text(self):
        return self.label.get_text()

    def set_text(self, text):
        self.label.set_text(text)

    def get_value(self):
        return self.switch.get_active()

    def set_value(self, value):
        old_value = self.switch.get_active()
        self.switch.set_active(value)

        if self.interface.on_change and old_value != value:
            self.interface.on_change(self.interface)

    def set_color(self, color):
        self.apply_css("color", get_color_css(color), native=self.native_label)

    def set_font(self, font):
        self.apply_css("font", get_font_css(font), native=self.native_label)

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(width[0])
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = height[1]
