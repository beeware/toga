from travertino.size import at_least

from toga_cocoa.libs import *

from .base import Widget


class ProgressBar(Widget):
    def create(self):
        self.native = NSProgressIndicator.new()
        self.native.style = NSProgressIndicatorBarStyle
        self.native.displayedWhenStopped = True

        # Add the layout constraints
        self.add_constraints()
        self.rehint()

    def set_value(self, value):
        if value is not None:
            self.native.doubleValue = value

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
            self.native.indeterminate = False
            self.native.maxValue = value
        else:
            self.native.indeterminate = True

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.fittingSize().height
