from pytest import skip, xfail

from toga_iOS.libs import UIButton

from .base import SimpleProbe
from .properties import toga_font


class ButtonProbe(SimpleProbe):
    native_class = UIButton

    @property
    def text(self):
        return str(self.native.title)

    @property
    def color(self):
        xfail("Can't get/set the text color of a button on iOS")

    @property
    def font(self):
        return toga_font(self.native.font)

    @property
    def background_color(self):
        skip("Background color not supported yet")
