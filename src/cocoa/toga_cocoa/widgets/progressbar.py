from toga.interface import ProgressBar as ProgressBarInterface

from ..libs import *
from .base import WidgetMixin


class ProgressBar(ProgressBarInterface, WidgetMixin):
    def __init__(self, id=None, style=None, max=None, value=None):
        super().__init__(id=id, style=style, max=max, value=value)
        self._create()

    def create(self):
        self._impl = NSProgressIndicator.new()
        self._impl.setStyle_(NSProgressIndicatorBarStyle)
        self._impl.setDisplayedWhenStopped_(True)

        # Add the layout constraints
        self._add_constraints()

    def _set_value(self, value):
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

    def _set_max(self, value):
        if value:
            self._impl.setIndeterminate_(False)
            self._impl.setMaxValue_(value)
        else:
            self._impl.setIndeterminate_(True)
