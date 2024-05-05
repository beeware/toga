from android.graphics import Color
from java import jclass

from .base import SimpleProbe
from .properties import assert_color, toga_color


class DividerProbe(SimpleProbe):
    native_class = jclass("android.view.View")

    def assert_background_color(self, color):
        actual_background_color = toga_color(self.native.getBackground().getColor())
        if color is None:
            assert_color(actual_background_color, toga_color(Color.LTGRAY))
        else:
            assert_color(actual_background_color, color)
