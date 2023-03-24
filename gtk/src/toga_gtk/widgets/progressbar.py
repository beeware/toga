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
    "A background task to animate running indeterminate progress bars"
    print("START PULSE")
    while True:
        progressbar.native.pulse()
        await asyncio.sleep(0.1)


class ProgressBar(Widget):
    def create(self):
        self.native = Gtk.ProgressBar()
        self.native.set_name(f"toga-{self.interface.id}")
        self.native.get_style_context().add_class("toga")
        self.native.interface = self.interface

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
        if self.get_max() is not None:
            self.native.set_fraction(value / self._max)

    def get_max(self):
        return self._max

    def set_max(self, value):
        self._max = value
        if self._max is None:
            if self._task is None:
                self._task = asyncio.create_task(pulse(self))
        else:
            if self._task:
                self._task.cancel()
                self._task = None

    def start(self):
        self._running = True
        if self._max is None:
            self._task = asyncio.create_task(pulse(self))

    def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None
            self.native.set_fraction(0.0)

    def rehint(self):
        # print("REHINT", self, self.native.get_preferred_width(), self.native.get_preferred_height())
        width = self.native.get_preferred_width()
        height = self.native.get_preferred_height()

        self.interface.intrinsic.width = at_least(width[0])
        self.interface.intrinsic.height = height[0]
