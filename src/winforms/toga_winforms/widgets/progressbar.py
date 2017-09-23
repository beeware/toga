from ..libs import *
from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = WinForms.ProgressBar()

    def start(self):
        '''Not supported for WinForms implementation'''
        pass

    def stop(self):
        '''Not supported for WinForms implementation'''
        pass

    def set_max(self, value):
        self.native.Maximum = value

    def set_value(self, value):
        self.native.Value = value

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.interface.style.hint(
            height=self.native.PreferredSize.Height,
            min_width=100,
        )
