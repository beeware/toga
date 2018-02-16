from gi.repository import Gtk, GObject

from .base import Widget
from travertino.size import at_least


class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()
        self.native.interface = self.interface

    def _pulse(self, *a, **kw):
        self.native.pulse()
        return not self.interface.max and self.interface.running

    def set_value(self, value):
        self.native.set_fraction(self.interface.value / self.interface.max)

    def set_max(self, value):
        if value:
            if self.interface.running:
                pass  # GTK has no 'working' animation
        else:
            if self.interface.running:
                GObject.timeout_add(60, self._pulse, None)

    def start(self):
        if self.interface.max:
            pass  # GTK has no 'working' animation
        else:
            GObject.timeout_add(60, self._pulse, None)

    def stop(self):
        pass

    def rehint(self):
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[1]
