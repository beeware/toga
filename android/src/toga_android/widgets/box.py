from android.widget import RelativeLayout

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = RelativeLayout(self._native_activity)
