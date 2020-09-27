from toga_cocoa.libs import (
    NSProgressIndicator,
    NSProgressIndicatorSpinningStyle
)

from .base import Widget


class ActivityIndicator(Widget):

    def create(self):
        self.native = NSProgressIndicator.new()
        self.native.style = NSProgressIndicatorSpinningStyle
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.displayedWhenStopped = False
        self.native.usesThreadedAnimation = True
        self.native.indeterminate = True
        self.native.bezeled = False
        self.native.sizeToFit()

        # Add the layout constraints
        self.add_constraints()
        self.rehint()

    def start(self):
        self.native.startAnimation(self.native)

    def stop(self):
        self.native.stopAnimation(self.native)
