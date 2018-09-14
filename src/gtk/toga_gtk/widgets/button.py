from gi.repository import Gtk
from travertino.size import at_least
from .base import Widget
from toga_gtk.libs.utils import gtk_apply_css


class Button(Widget):
    def create(self):
        self.native = Gtk.Button()
        self.native.interface = self.interface
        self.native.connect('show', lambda event: self.rehint())
        self.native.connect('clicked', self.on_press)

    def set_label(self, label):
        self.native.set_label(self.interface.label)
        self.rehint()

    def set_enabled(self, value=True):
        super(Button, self).set_enabled(value)

    def set_background_color(self, value):
        if value:
            gtk_apply_css(self.native, {"background-color": value})

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]

    def on_press(self, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)
