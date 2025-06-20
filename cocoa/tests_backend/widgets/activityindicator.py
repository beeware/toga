from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = NSProgressIndicator

    def assert_is_hidden(self, value):
        # Check that we're not displaying the widget when stopped.
        assert not self.native.isDisplayedWhenStopped()
        # No other action nessacary otherwise, as there's no way to
        # see if the widget is stopped.
