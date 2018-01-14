from gi.repository import Gtk

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()
        self.native.interface = self.interface

    def set_value(self, value):
        if value is not None:
            self.interface._running = self.interface.value is not None
            self.native.set_fraction(float(self.interface.value) / float(self.interface.max))

    def start(self):
        if not self.interface._running:
            self.interface._running = True

    def stop(self):
        if self.interface._running:
            self.interface._running = False

    def set_max(self, value):
        # No special handling required
        pass
