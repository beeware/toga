from android.widget import RelativeLayout

from toga.colors import TRANSPARENT

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = RelativeLayout(self._native_activity)

    def set_background_color(self, color):
        self.set_background_simple(TRANSPARENT if color is None else color)
