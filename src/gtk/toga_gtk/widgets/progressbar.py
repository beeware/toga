import threading
from gi.repository import Gtk

from .base import Widget


def interval(period, f, *a, **kw):
    stop_event = threading.Event()

    def stop():
        stop_event.set()

    def run():
        f(*a, **kw)
        if not stop_event.is_set():
            t = threading.Timer(period, run)
            t.daemon = True
            t.start()

    run()
    return stop

PROGRESSBAR_TICK_INTERVAL = 0.1 # seconds per tick

class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()
        self.native.interface = self.interface

    def _tick(self):
        self.native.pulse()

    def _render_disabled(self):
        self.native.set_fraction(0)

    def set_value(self, value):
        self.native.set_fraction(self.interface.value / self.interface.max)

    def set_max(self, value):
        if not self.interface.enabled:
            self._render_disabled()

    def start(self):
        def tick():
            self.native.pulse()

        self.stop_animation = interval(PROGRESSBAR_TICK_INTERVAL, tick)

    def stop(self):
        self.stop_animation()

        def reset():
            if self.interface.enabled:
                # set_value uses self.interface.value, not the parameter.
                # Therefore, passing None does NOT change the value to None, but it
                # will put the native widget back into determinate mode.
                self.set_value(None)
            else:
                # handle disabled state manually
                self._render_disabled()

        # If `reset()` should be scheduled for two tick intervals in the
        # future to guarantee that it will execute after the last tick,
        # otherwise the last tick will put the native progress bar back in pulsing
        # mode.
        threading.Timer(PROGRESSBAR_TICK_INTERVAL * 2, reset).start()
