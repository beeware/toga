from travertino.size import at_least

from toga_cocoa.libs import NSProgressIndicator, NSProgressIndicatorBarStyle

from .base import Widget

# Implementation notes
# ====================
#
# * Cocoa doesn't have a way to determine if the animation is running. We track
#   running status independently for interface compliance.


class ProgressBar(Widget):
    def create(self):
        self.native = NSProgressIndicator.new()
        self.native.style = NSProgressIndicatorBarStyle
        self.native.displayedWhenStopped = True
        self.native.usesThreadedAnimation = False

        # Add the layout constraints
        self.add_constraints()

        self._is_running = False

    def is_running(self):
        return self._is_running

    def get_value(self):
        if self.native.isIndeterminate():
            return None
        return float(self.native.doubleValue)

    def set_value(self, value):
        self.native.doubleValue = value

    def start(self):
        self.native.startAnimation(self.native)
        self._is_running = True

    def stop(self):
        self.native.stopAnimation(self.native)
        self._is_running = False

    def get_max(self):
        if self.native.isIndeterminate():
            return None
        return float(self.native.maxValue)

    def set_max(self, value):
        if value is None:
            self.native.doubleValue = 0.0
            self.native.indeterminate = True
            if self.is_running():
                self.start()
            else:
                self.stop()
        else:
            self.native.indeterminate = False
            self.native.maxValue = value

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = self.native.intrinsicContentSize().height
