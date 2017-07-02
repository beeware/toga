from ..libs import *
from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = NSProgressIndicator.new()
        self.native.setStyle_(NSProgressIndicatorBarStyle)
        self.native.setDisplayedWhenStopped_(True)

        # Add the layout constraints
        self.add_constraints()

    def set_value(self, value):
        if value is not None:
            self.native.setDoubleValue_(value)

    def start(self):
        if self.native and not self.interface._running:
            self.native.startAnimation(self.native)
            self.interface._running = True

    def stop(self):
        if self.native and self.interface._running:
            self.native.stopAnimation(self.native)
            self.interface._running = False

    def set_max(self, value):
        if value:
            self.native.setIndeterminate_(False)
            self.native.setMaxValue_(value)
        else:
            self.native.setIndeterminate_(True)
