from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ProgressBarProbe(SimpleProbe):
    native_class = NSProgressIndicator

    @property
    def is_determinate(self):
        return not self.native.isIndeterminate()

    @property
    def is_animating_indeterminate(self):
        # Cocoa doesn't require any explicit animation flags
        return not self.is_determinate and self.widget._impl._is_running

    @property
    def position(self):
        return float(self.native.doubleValue / self.native.maxValue)

    async def wait_for_animation(self):
        # Cocoa ProgressBar has internal animation handling; no special handling required.
        pass
