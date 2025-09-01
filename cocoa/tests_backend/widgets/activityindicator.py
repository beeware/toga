from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = NSProgressIndicator

    def assert_spinner_is_hidden(self, value):
        # Check that the widget is correctly configured to *not* display the widget when
        # stopped. We can't verify the *actual* visibility status, as we can't inspect
        # the internal state of the spinner.
        assert not self.native.isDisplayedWhenStopped()
        is_visible = self.impl._is_running and not self.native.isHidden()
        assert is_visible == (not value)
