from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()

    def start(self):
        self.set_running_style()

    def stop(self):
        self.set_stopping_style()

    @property
    def max(self):
        return self.interface.max

    def set_max(self, value):
        if value is not None:
            self.native.Maximum = value
        if self.interface.is_running:
            self.set_running_style()
        else:
            self.set_stopping_style()

    def set_running_style(self):
        if self.max is None:
            self.native.Style = WinForms.ProgressBarStyle.Marquee
        else:
            self.native.Style = WinForms.ProgressBarStyle.Blocks

    def set_stopping_style(self):
        self.native.Style = WinForms.ProgressBarStyle.Continuous

    def set_value(self, value):
        self.native.Value = value

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
