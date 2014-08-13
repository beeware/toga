from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget
from toga.constants import *


class ProgressBar(Widget):
    def __init__(self, max=None, value=None):
        super(ProgressBar, self).__init__()
        self.max = max

        self.startup()

        self.value = value

    def startup(self):
        self._impl = NSProgressIndicator.new()
        self._impl.setStyle_(NSProgressIndicatorBarStyle)
        self._impl.setDisplayedWhenStopped_(False)
        if self.max:
            self._impl.setIndeterminate_(False)
            self._impl.setMaxValue_(self.max)
        else:
            self._impl.setIndeterminate_(True)

        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._running = self._value is not None
        if value is not None:
            self._impl.setDoubleValue_(value)

    def start(self):
        if self._impl and not self._running:
            self._impl.startAnimation_(self._impl)
            self._running = True

    def stop(self):
        if self._impl and self._running:
            self._impl.stopAnimation_(self._impl)
            self._running = False
