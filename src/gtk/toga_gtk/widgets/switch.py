from gi.repository import Gtk
from travertino.size import at_least

from .base import Widget


class Switch(Widget):
    def create(self):
        self._on_toggle_handler = None

        self.native = Gtk.Box()
        self.native.interface = self.interface

        self.label = Gtk.Label(xalign=0)
        self.label.set_line_wrap(True)

        self.switch = Gtk.Switch()
        self.switch.connect("notify::active", self._on_toggle)

        self.native.pack_start(self.label, True, True, 0)
        self.native.pack_start(self.switch, False, False, 0)
        self.native.connect('show', lambda event: self.rehint())

    def _on_toggle(self, widget, state):
        if self._on_toggle_handler:
            self._on_toggle_handler(widget)

    def set_on_toggle(self, handler):
        self._on_toggle_handler = handler

    def set_label(self, label):
        self.label.set_text(label)

    def get_is_on(self):
        return self.switch.get_active()

    def set_is_on(self, value):
        self.switch.set_active(value)

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        # Set intrinsic width to at least the minimum width
        self.interface.intrinsic.width = at_least(width[0])
        # Set intrinsic height to the natural height
        self.interface.intrinsic.height = height[1]
