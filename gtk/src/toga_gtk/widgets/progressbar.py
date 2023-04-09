import asyncio

from travertino.size import at_least

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
    """A background task to animate running indeterminate progress bars"""
    while True:
        progressbar.native.pulse()
        await asyncio.sleep(0.1)


class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()

        self._max = 1.0
        self._running = False
        self._task = None

    def is_running(self):
        return self._running

    def get_value(self):
        if self.get_max() is None:
            return None
        return self.native.get_fraction() * self._max

    def set_value(self, value):
        self.native.set_fraction(value / self._max)

    def get_max(self):
        return self._max

    def _start_indeterminate(self):
        self._task = asyncio.create_task(pulse(self))

    def _stop_indeterminate(self):
        if self._task:
            self._task.cancel()
            self._task = None
            self.native.set_fraction(0.0)

    def set_max(self, value):
        if value is None:
            self._max = None
            self.native.set_fraction(0.0)
            if self.is_running():
                self._start_indeterminate()
            else:
                self._stop_indeterminate()
        else:
            if self._max is None:
                # Switching from indeterminate to determinate mode.
                # Any value will be nonsensical, so set the current value
                # to 0.
                self.native.set_fraction(0.0)
            else:
                # Adjust the displayed fraction to reflect the new max.
                self.native.set_fraction(self.native.get_fraction() * self._max / value)
            self._max = value
            self._stop_indeterminate()

    def start(self):
        self._running = True
        if self._max is None:
            self._start_indeterminate()

    def stop(self):
        self._running = False
        self._stop_indeterminate()

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[0]
