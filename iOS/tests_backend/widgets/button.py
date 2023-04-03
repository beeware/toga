from toga_iOS.libs import UIButton, UIControlStateNormal

from .base import SimpleProbe
from .properties import toga_color, toga_font


class ButtonProbe(SimpleProbe):
    native_class = UIButton

    @property
    def text(self):
        return str(self.native.titleForState(UIControlStateNormal))

    @property
    def color(self):
        return toga_color(self.native.titleColorForState(UIControlStateNormal))

    @property
    def font(self):
        return toga_font(self.native.titleLabel.font)

    @property
    def background_color(self):
        return toga_color(self.native.backgroundColor)
