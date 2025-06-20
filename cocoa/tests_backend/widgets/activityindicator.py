import pytest

from toga_cocoa.libs import NSProgressIndicator

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = NSProgressIndicator

    def assert_is_hidden(self, value):
        if self.native.isDisplayedWhenStopped():
            pytest.fail(
                "ActivityIndicator should not be displayed when stopped on macOS"
            )
        # No other action nessacary otherwise, as there's no way to
        # see if the widget is stopped.
