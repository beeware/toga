from gi.repository import Gtk, GObject

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()
        self.native.interface = self.interface
        self.timeout_id = GObject.timeout_add(50, self._animate, None)

    def _animate(self, *a, **kw):
        if self.interface.running:
            self.native.pulse()

        return True

    def set_value(self, value):
        self.native.set_fraction(value / self.interface.max)

    def set_max(self, value):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def rehint(self):
        size = self.native.size_request()
        self.interface.style.hint(
            min_width=size.width,
            min_height=size.height
        )
