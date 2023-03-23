import asyncio

from ..libs import Gtk
from .base import Widget

# Implementation notes
# ====================
#
# * GTK ProgressBar doesn't have any concept of running; we track the running
#   status for API compliance.
#
# * Indeterminate GTK ProgressBars need to be manually animated; when an
#   indeterminate progress bar is started, we add a background task to do this
#   pulse animation every 100ms.
#
# * GTK ProgressBar uses 0-1 floating point range. We track the Toga max value
#   internally for scaling purposes.


async def pulse(progressbar):
    "A background task to animate running indeterminate progress bars"
    while True:
        progressbar.native.pulse()
        asyncio.sleep(100)


class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()
        self.native.interface = self.interface

        self._max = 1.0
        self._running = False
        self._task = None

    def get_value(self):
        if self.get_max() is None:
            return None

        return self.native.get_fraction() * self._max

    def set_value(self, value):
        if self.get_max() is not None:
            self.native.set_fraction(value / self._max)

    def get_max(self):
        return self._max

    def set_max(self, value):
        self._max = value

    def start(self):
        self._running = True
        if self._max is None:
            self._task = asyncio.create_task(pulse(self))

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            self.native.set_fraction(0.0)
