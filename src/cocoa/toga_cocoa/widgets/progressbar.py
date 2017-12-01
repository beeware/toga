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
        self.native.doubleValue = value

    def start(self):
        self.native.startAnimation(self.native)

    def stop(self):
        self.native.stopAnimation(self.native)

    def set_max(self, value):
        if value:
            self.native.indeterminate = False
            self.native.maxValue = value
        else:
            self.native.indeterminate = True

    def rehint(self):
        self.interface.style.hint(
            height=self.native.fittingSize().height,
            min_width=100
        )
