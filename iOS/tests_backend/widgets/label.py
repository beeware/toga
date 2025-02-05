from toga_iOS.libs import UILabel

from .base import SimpleProbe
from .properties import toga_color, toga_text_align


class LabelProbe(SimpleProbe):
    native_class = UILabel

    @property
    def text(self):
        value = str(self.native.text)
        if value == "\u200b":
            return ""
        return value

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def text_align(self):
        return toga_text_align(self.native.textAlignment)

    def assert_vertical_text_align(self, alignment):
        # iOS has a custom draw method that always draw the text at the top;
        # this location isn't configurable
        pass
