from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget

# Implementation notes
# ====================
#
# * Inactive Winforms ProgressBars have a distinct style. We use that style as an
#   indicator for whether the ProgressBar is running.
#
# * ProgressBar uses an integer to track for progress. Toga's values are
#   floats; so we multiply the Toga value by 1000 so that we get 3dp of
#   functional progress fidelity.
#
# * There's no native way to identify an indeterminate progress bar. We can't
#   use a max value of 0 as a marker, because a max value of 0 causes the the
#   animation to stop. Therefore, we track indeterminate status independently.


class ProgressBar(Widget):
    TOGA_SCALE = 1000

    def create(self):
        self.native = WinForms.ProgressBar()
        self.set_stopping_style()

        self._determinate = True

    def is_running(self):
        return self.native.Style != WinForms.ProgressBarStyle.Continuous

    def start(self):
        self.set_running_style()

    def stop(self):
        self.set_stopping_style()

    def get_max(self):
        if not self._determinate:
            return None
        return float(self.native.Maximum / self.TOGA_SCALE)

    def set_max(self, value):
        if value is None:
            self.native.Maximum = 1000
            self._determinate = False
        else:
            self.native.Maximum = int(value * self.TOGA_SCALE)
            self._determinate = True

        if self.is_running():
            self.set_running_style()
        else:
            self.set_stopping_style()

    def set_running_style(self):
        if not self._determinate:
            self.native.Style = WinForms.ProgressBarStyle.Marquee
        else:
            self.native.Style = WinForms.ProgressBarStyle.Blocks

    def set_stopping_style(self):
        self.native.Style = WinForms.ProgressBarStyle.Continuous

    def get_value(self):
        if not self._determinate:
            return None

        return float(self.native.Value / self.TOGA_SCALE)

    def set_value(self, value):
        if self._determinate:
            self.native.Value = int(value * self.TOGA_SCALE)

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
