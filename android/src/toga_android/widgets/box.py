from travertino.size import at_least

from android.widget import RelativeLayout

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = RelativeLayout(self._native_activity)

    def set_background_color(self, value):
        self.set_background_simple(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
