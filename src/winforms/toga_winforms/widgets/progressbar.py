from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()
        # Windows expects integers provide 3 decimal precision for % resolution
        self.native.Maximum = 1000

    def start(self):
        '''Not supported for WinForms implementation'''
        self.interface.factory.not_implemented('ProgressBar.start()')

        # possible implementation (not tested):
        # self.native.Style = ProgressBarStyle.Marquee

    def stop(self):
        '''Not supported for WinForms implementation'''
        self.interface.factory.not_implemented('ProgressBar.stop()')

        # possible implementation (not tested):
        # self.native.Style = ProgressBarStyle.Continuous

    def set_max(self, value):
        self.interface.factory.not_implemented('ProgressBar.set_max()')

    def set_value(self, value):
        if value is None:
            value = self.native.Minimum
        if not isinstance(value, float):
            value = float(value)
        # convert to integer that is % of max.
        value = int(value * self.native.Maximum)
        if value > self.native.Maximum:
            value = self.native.Maximum
        if value < self.native.Minimum:
            value = self.native.Minimum
        self.native.Value = value

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
