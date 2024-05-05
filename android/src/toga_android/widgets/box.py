from android.widget import RelativeLayout

from toga.colors import TRANSPARENT

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = RelativeLayout(self._native_activity)

    def set_background_color(self, value):
        if value is None:
            self.set_background_simple(TRANSPARENT)
        else:
            self.set_background_simple(value)
