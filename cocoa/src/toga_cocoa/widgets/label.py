from travertino.size import at_least

from toga_cocoa.colors import native_color
from toga_cocoa.libs import NSTextAlignment, NSTextField

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = NSTextField.alloc().init()

        self.native.drawsBackground = False
        self.native.editable = False
        self.native.bezeled = False

        # Add the layout constraints
        self.add_constraints()

    def set_alignment(self, value):
        self.native.alignment = NSTextAlignment(value)

    def set_color(self, value):
        self.native.textColor = native_color(value)

    def set_font(self, font):
        self.native.font = font._impl.native

    def get_text(self):
        return str(self.native.stringValue)

    def set_text(self, value):
        self.native.stringValue = value

    def rehint(self):
        # Width & height of a label is known and fixed.
        content_size = self.native.intrinsicContentSize()
        # print("REHINT label", self, content_size.width, content_size.height)
        # 2020-05-11 The +1 is a hack; the label "X Translate:" gets truncated
        # without the extra pixel.
        self.interface.intrinsic.width = at_least(content_size.width + 1)
        self.interface.intrinsic.height = content_size.height
