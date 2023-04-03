from travertino.size import at_least

from ..libs import Gtk, get_color_css, get_font_css
from .base import Widget


class Switch(Widget):
    SPACING = 10

    def create(self):
        self.native = Gtk.Box(spacing=self.SPACING)

        self.native_label = Gtk.Label(xalign=0)
        self.native_label.set_name(f"toga-{self.interface.id}-label")
        self.native_label.get_style_context().add_class("toga")
        self.native_label.set_line_wrap(False)

        self.native_switch = Gtk.Switch()
        self.native_switch.set_name(f"toga-{self.interface.id}-switch")
        self.native_switch.get_style_context().add_class("toga")
        self.native_switch.connect("notify::active", self.gtk_notify_active)

        self.native.pack_start(self.native_label, True, True, 0)
        self.native.pack_start(self.native_switch, False, False, 0)

    def gtk_notify_active(self, widget, state):
        self.interface.on_change(None)

    def get_enabled(self):
        return self.native_switch.get_sensitive()

    def set_enabled(self, value):
        self.native_label.set_sensitive(value)
        self.native_switch.set_sensitive(value)

    def get_text(self):
        return self.native_label.get_text()

    def set_text(self, text):
        self.native_label.set_text(text)

    def get_value(self):
        return self.native_switch.get_active()

    def set_value(self, value):
        self.native_switch.set_active(value)

    def set_color(self, color):
        self.apply_css("color", get_color_css(color), native=self.native_label)

    def set_font(self, font):
        self.apply_css("font", get_font_css(font), native=self.native_label)

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        label_width = self.native_label.get_preferred_width()
        label_height = self.native_label.get_preferred_height()

        switch_width = self.native_switch.get_preferred_width()
        switch_height = self.native_switch.get_preferred_height()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(
            label_width[0] + self.SPACING + switch_width[0]
        )
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = max(label_height[1], switch_height[1])
