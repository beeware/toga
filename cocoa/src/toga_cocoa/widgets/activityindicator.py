from toga_cocoa.libs import NSProgressIndicator, NSProgressIndicatorSpinningStyle

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

        # Cocoa doesn't provide a way to determine if the animation is currently
        # running; proxy the state
        self._is_running = False

        # Add the layout constraints
        self.add_constraints()

    def is_running(self):
        return self._is_running

    def start(self):
        self.native.startAnimation(self.native)
        self._is_running = True

    def stop(self):
        self.native.stopAnimation(self.native)
        self._is_running = False

    def rehint(self):
        self.interface.intrinsic.width = self.native.intrinsicContentSize().width
        self.interface.intrinsic.height = self.native.intrinsicContentSize().height
