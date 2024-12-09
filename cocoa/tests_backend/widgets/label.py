from toga_cocoa.libs import NSTextField

from .base import SimpleProbe
from .properties import toga_color, toga_text_alignment


class LabelProbe(SimpleProbe):
    native_class = NSTextField

    @property
    def text(self):
        return str(self.native.stringValue)

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def text_alignment(self):
        return toga_text_alignment(self.native.alignment)

    def assert_vertical_text_alignment(self, expected):
        # Vertical alignment isn't configurable on NSTextField
        pass
