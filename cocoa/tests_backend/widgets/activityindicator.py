from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = NSProgressIndicator

    @property
    def is_running(self):
        # Cocoa doesn't have a native concept of running;
        # use the impl's proxy representation.
        return self.widget._impl._is_running
