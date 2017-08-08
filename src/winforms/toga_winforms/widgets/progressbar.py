from __future__ import print_function, absolute_import, division

from toga.interface import ProgressBar as ProgressBarInterface

from ..libs import *

from .base import WidgetMixin

class ProgressBar(ProgressBarInterface, WidgetMixin):
    def __init__(self, id=None, style=None, max=100, value=0):
        super(ProgressBarInterface, self).__init__(
                id=id, style=style, max=max, value=value)

        self._create()

    def create(self):
        self._impl = WinForms.ProgressBar()
        self._marquee_animation_speed = self._impl.MarqueeAnimationSpeed

    def start(self):
        '''Not supported for WinForms implementation'''
        pass

    def stop(self):
        '''Not supported for WinForms implementation'''
        pass

    @property
    def max(self):
        return self._impl.Maximum

    @max.setter
    def max(self, max):
        self._impl.Maximum = max

    @property
    def value(self):
        return self._impl.Value

    @value.setter
    def value(self, value):
        self._impl.Value = value

    def rehint(self):
        # Height must be non-zero
        # Set a sensible min-width
        self.style.hint(
            height=self._impl.PreferredSize.Height,
            min_width=100,
            )
