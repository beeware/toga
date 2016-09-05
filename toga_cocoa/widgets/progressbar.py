from toga.interface import ProgressBar as ProgressBarInterface

from ..libs import *
from .base import WidgetMixin


class ProgressBar(ProgressBarInterface, WidgetMixin):
    def __init__(self, id=None, style=None, max=None, value=None):
        super().__init__(id=None, style=None, max=None, value=None)
        self.startup()

    def startup(self):
        self._impl = NSProgressIndicator.new()
        self._impl.setStyle_(NSProgressIndicatorBarStyle)
        self._impl.setDisplayedWhenStopped_(True)
        if self.max:
            self._impl.setIndeterminate_(False)
            self._impl.setMaxValue_(self.max)
        else:
            self._impl.setIndeterminate_(True)

        # Add the layout constraints
        self._add_constraints()

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
