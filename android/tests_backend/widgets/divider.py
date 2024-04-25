from android.graphics import Color
from android.graphics.drawable import ColorDrawable
from java import jclass

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = jclass("android.view.View")

    @property
    def background_color(self):
        background = self.native.getBackground()
        if isinstance(background, ColorDrawable) and (
            background.getColor() == Color.LTGRAY
        ):
            return None
        else:
            return super().background_color
