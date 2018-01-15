from travertino.size import at_least

from toga_winforms.libs import *

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()

    def start(self):
        '''Not supported for WinForms implementation'''
        raise NotImplementedError()

    def stop(self):
        '''Not supported for WinForms implementation'''
        raise NotImplementedError()

    def set_max(self, value):
        self.native.Maximum = value

    def set_value(self, value):
        self.native.Value = value

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
