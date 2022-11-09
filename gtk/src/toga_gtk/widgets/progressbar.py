from ..libs import GLib, Gtk
from .base import Widget

PROGRESSBAR_TICK_INTERVAL = 100  # ms per tick


class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()
        self.native.interface = self.interface

    def _render_disabled(self):
        self.native.set_fraction(0)

    def set_value(self, value):
        self.native.set_fraction(self.interface.value / self.interface.max)

    def set_max(self, value):
        if not self.interface.enabled:
            self._render_disabled()

    def start(self):
        def tick(*a, **kw):
            self.native.pulse()
            return not self.interface.is_determinate

        if not self.interface.is_determinate:
            GLib.timeout_add(PROGRESSBAR_TICK_INTERVAL, tick, None)

    def stop(self):
        def restore_fraction():
            if self.interface.enabled:
                # set_value uses self.interface.value, not the parameter.
                # Therefore, passing None does NOT change the value to None, but it
                # will put the native widget back into determinate mode.
                self.set_value(None)
            else:
                # handle disabled state manually
                self._render_disabled()
            return False

        # If `restore_fraction()` is scheduled for two tick intervals in the
        # future to guarantee that it will execute after the last tick,
        # otherwise the last tick will put the native progress bar back in pulsing
        # mode.
        GLib.timeout_add(PROGRESSBAR_TICK_INTERVAL * 2, restore_fraction)
