from toga_iOS.libs import UILabel

from .base import SimpleProbe
from .properties import toga_color, toga_text_alignment


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
    def text_alignment(self):
        return toga_text_alignment(self.native.textAlignment)

    def assert_vertical_text_alignment(self, alignment):
        # iOS has a custom draw method that always draw the text at the top;
        # this location isn't configurable
        pass
