from java import jclass
from pytest import skip

from .base import SimpleProbe
from .properties import toga_color


class LabelProbe(SimpleProbe):
    native_class = jclass("android.widget.TextView")

    @property
    def color(self):
        return toga_color(self.native.getCurrentTextColor())

    @property
    def text(self):
        return str(self.native.getText())

    @property
    def font(self):
        skip("Font probe not implemented")

    @property
    def alignment(self):
        skip("Alignment probe not implemented")
