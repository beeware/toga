from toga_iOS.libs import UIButton, UIControlStateNormal

from .base import SimpleProbe
from .properties import toga_color


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
        return self.native.titleLabel.font
