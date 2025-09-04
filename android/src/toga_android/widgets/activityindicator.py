from android import R
from android.view import View
from android.widget import ProgressBar

from .base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = ProgressBar(
            self._native_activity,
            None,
            R.attr.progressBarStyleSmall,
        )
        # Always set as running and we just control visibility.
        self.native.setIndeterminate(True)
        self._running = False
        self._hidden = False

    def is_running(self):
        return self._running

    def start(self):
        self._running = True
        self.native.setVisibility(View.INVISIBLE if self._hidden else View.VISIBLE)

    def stop(self):
        self._running = False
        self.native.setVisibility(View.INVISIBLE)

    def set_hidden(self, hidden):
        if hidden or not self._running:
            self.native.setVisibility(View.INVISIBLE)
        else:
            self.native.setVisibility(View.VISIBLE)
        self._hidden = hidden

    def rehint(self):
        self.native.measure(
            View.MeasureSpec.UNSPECIFIED,
            View.MeasureSpec.UNSPECIFIED,
        )
        self.interface.intrinsic.width = self.native.getMeasuredWidth()
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
