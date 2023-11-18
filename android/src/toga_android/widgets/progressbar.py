from decimal import ROUND_UP

from android import R
from android.view import View
from android.widget import ProgressBar as A_ProgressBar

from .base import Widget

# Implementation notes
# ====================
#
# * Android ProgressBar doesn't have a "running" mode; the closest it gets is
#   "animating", which only really applies to indeterminate progress bars. We
#   track running status independently for interface compliance.
#
# * Android ProgressBar has an "indeterminate" mode, but that's really a proxy
#   for "am I animating", not "am I an indeterminate progress bar". The
#   setIndeterminate() API essentially needs to be used as "start/stop
#   indeterminate animation". This needs to be invoked on start/stop, but also
#   when we move into an indeterminate state when already running.
#   setIndeterminate(False) can be safely called on non-determinate progress bars.
#
# * There's no native way to identify a stopped indeterminate progress bar. We
#   use a max value of 0 as a marker for an indeterminate progress bar. This
#   value won't be legal from the Toga interface, as Toga requires a positive
#   max value.
#
# * Android ProgressBar uses an integer to track for progress. Toga's values are
#   floats; so we multiply the Toga value by 1000 so that we get 3dp of
#   functional progress fidelity.


class ProgressBar(Widget):
    TOGA_SCALE = 1000

    def create(self):
        progressbar = A_ProgressBar(
            self._native_activity, None, R.attr.progressBarStyleHorizontal
        )
        self.native = progressbar

        self._running = False

    def is_running(self):
        return self._running

    def start(self):
        self._running = True
        if self.get_max() is None:
            self.native.setIndeterminate(True)

    def stop(self):
        self._running = False
        self.native.setIndeterminate(False)

    def get_max(self):
        # Indeterminate progress bar; return a max of None.
        if self.native.getMax() == 0:
            return None

        return float(self.native.getMax() / self.TOGA_SCALE)

    def set_max(self, value):
        if value is None:
            # Indeterminate progress bar; set the max to the marker value of 0,
            # and ensure that the bar won't show any meaningful progress value.
            self.native.setProgress(0)
            self.native.setMax(0)

            # If we're already running, put the bar into
            # indeterminate animation mode.
            if self._running:
                self.start()
            else:
                self.stop()
        else:
            # Make sure we're not in indeterminate mode. Android's
            # indeterminate mode is really an "is animating indeterminate",
            # so we don't care whether we're running or not.
            self.native.setIndeterminate(False)
            self.native.setMax(int(value * self.TOGA_SCALE))

    def get_value(self):
        if self.native.getMax() == 0:
            return None
        return float(self.native.getProgress() / self.TOGA_SCALE)

    def set_value(self, value):
        self.native.setProgress(int(value * self.TOGA_SCALE))

    def rehint(self):
        self.native.measure(
            View.MeasureSpec.UNSPECIFIED,
            View.MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.height = self.scale_out(
            self.native.getMeasuredHeight(), ROUND_UP
        )
