from android import R
from android.widget import ProgressBar
from android.view import View
from .base import Widget

class ActivityIndicator(Widget):
    def create(self):
        self.native = ProgressBar(
            self._native_activity, 
            None, 
            R.attr.progressBarStyle
        )
        self.native.setIndeterminate(False)
        self._running = False

    def is_running(self):
        return self._running

    def start(self):
        self._running = True
        self.native.setVisibility(View.VISIBLE)
        # Indeterminate means it's animating.
        self.native.setIndeterminate(True)

    def stop(self):
        self._running = False
        self.native.setVisibility(View.GONE)
        self.native.setIndeterminate(False)

    def set_hidden(self, hidden):
        if hidden or not self._running:
            self.native.setVisibility(View.GONE)
        else:
            self.native.setVisibility(View.VISIBLE)

    def rehint(self):
        self.native.measure(
            View.MeasureSpec.UNSPECIFIED,
            View.MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = self.native.getMeasuredWidth()
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
