from android.view import View
from android.widget import ProgressBar

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = ProgressBar

    def assert_is_hidden(self, value):
        assert self.native.getVisibility() == (
            View.INVISIBLE if value else View.VISIBLE
        )
