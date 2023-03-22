from toga.colors import TRANSPARENT
from toga_iOS.libs import UIColor, UILabel

from .base import SimpleProbe
from .properties import toga_alignment, toga_color, toga_font


class LabelProbe(SimpleProbe):
    native_class = UILabel

    @property
    def text(self):
        value = str(self.native.text)
        if value == "\u200B":
            return ""
        return value

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def background_color(self):
        if self.native.backgroundColor == UIColor.clearColor:
            return TRANSPARENT
        else:
            return toga_color(self.native.backgroundColor)

    @property
    def font(self):
        return toga_font(self.native.font)

    @property
    def alignment(self):
        return toga_alignment(self.native.textAlignment)
