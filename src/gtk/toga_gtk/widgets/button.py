from travertino.size import at_least

from ..libs import (
    Gtk,
    apply_gtk_style,
    get_color_css,
    get_bg_color_css,
    get_font_css
)
from .base import Widget


class Button(Widget):
    def create(self):
        self.native = Gtk.Button()
        self.native.interface = self.interface

        self.native.connect('show', lambda event: self.rehint())
        self.native.connect('clicked', self.gtk_on_press)

    def set_label(self, label):
        self.native.set_label(self.interface.label)
        self.rehint()

    def set_enabled(self, value):
        self.native.set_sensitive(value)

    def set_color(self, color):
        if color:
            style_context = self.native.get_style_context()
            css = get_color_css(color)
            apply_gtk_style(style_context, css, "toga-color")

    def set_background_color(self, color):
        if color:
            style_context = self.native.get_style_context()
            css = get_bg_color_css(color)
            apply_gtk_style(style_context, css, "toga-bg-color")

    def set_font(self, value):
        if value:
            style_context = self.native.get_style_context()
            css = get_font_css(value)
            apply_gtk_style(style_context, css, "toga-font")

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]

    def gtk_on_press(self, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)
