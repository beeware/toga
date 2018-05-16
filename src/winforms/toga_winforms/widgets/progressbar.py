from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()

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
        self.native.Maximum = value

    def set_value(self, value):
        self.native.Value = value

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
