from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = NSProgressIndicator

    @property
    def is_determinate(self):
        return not self.native.isIndeterminate()

    @property
    def is_animating_indeterminate(self):
        # Cocoa doesn't require any explicit animation flags required
        return not self.is_determinate and self.widget._impl._is_running
