from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = NSProgressIndicator

    def assert_is_hidden(self, value):
        # Check that we're not displaying the widget when stopped.
        assert not self.native.isDisplayedWhenStopped()
        # No other assertion is possible, as there's no way to verify
        # if the underlying widget is visible.
