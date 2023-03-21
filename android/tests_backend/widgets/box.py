from java import jclass

from .base import SimpleProbe
from .properties import toga_color


class BoxProbe(SimpleProbe):
    native_class = jclass("android.widget.RelativeLayout")

    @property
    def background_color(self):
        return toga_color(self.native.getBackground().getColor())
