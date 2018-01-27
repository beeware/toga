from gi.repository import Gtk, GObject

from .base import Widget


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
                pass # GTK has no 'working' animation
        else:
            if self.interface.running:
                GObject.timeout_add(60, self._pulse, None)

    def set_running(self, value):
        if value:
            if self.interface.max:
                pass # GTK has no 'working' animation
            else:
                GObject.timeout_add(60, self._pulse, None)

    def rehint(self):
        size = self.native.size_request()
        self.interface.style.hint(
            min_width=size.width,
            min_height=size.height
        )
