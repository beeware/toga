from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget

# Implementation notes
# ====================
#
# * Inctive Winforms ProgrssBars have a distinct style. We use that style
#   as an indicator for whether the ProgressBbar is running.


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()
        self.set_stopping_style()

    def is_running(self):
        return self.native.Style == WinForms.ProgressBarStyle.Continuous

    def start(self):
        self.set_running_style()

    def stop(self):
        self.set_stopping_style()

    def get_max(self):
        return self.native.Maximum

    def set_max(self, value):
        self.native.Maximum = value

        if self._is_running:
            self.set_running_style()
        else:
            self.set_stopping_style()

    def set_running_style(self):
        if self.get_max() is None:
            self.native.Style = WinForms.ProgressBarStyle.Marquee
        else:
            self.native.Style = WinForms.ProgressBarStyle.Blocks

    def set_stopping_style(self):
        self.native.Style = WinForms.ProgressBarStyle.Continuous

    def get_value(self):
        if self._max is None:
            return None

        return self.native.Value

    def set_value(self, value):
        if self._max is not None:
            self.native.Value = value

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
