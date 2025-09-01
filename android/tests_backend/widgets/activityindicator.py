from android.view import View
from android.widget import ProgressBar

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = ProgressBar

    def assert_spinner_is_hidden(self, value):
        is_visible = self.native.getVisibility() == View.VISIBLE
        assert is_visible == (not value)
