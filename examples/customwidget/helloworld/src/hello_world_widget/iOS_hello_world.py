from math import ceil

from rubicon.objc import NSMakeRect
from travertino.size import at_least

from toga_iOS.colors import native_color
from toga_iOS.libs import (
    NSLineBreakByClipping,
    NSTextAlignment,
)
from toga_iOS.widgets.base import Widget
from toga_iOS.widgets.label import TogaLabel


class HelloWorld(Widget):
    def create(self):
        self.native = TogaLabel.new()
        self.native.text = "Hello World!"
        self.native.numberOfLines = 1

        # We shouldn't ever word wrap; if faced with that option, clip.
        self.native.lineBreakMode = NSLineBreakByClipping

        # Add the layout constraints
        self.add_constraints()

    def set_text_align(self, value):
        self.native.textAlignment = NSTextAlignment(value)

    def set_color(self, value):
        self.native.textColor = native_color(value)

    def set_font(self, font):
        self.native.font = font._impl.native

    def rehint(self):
        # Ask the widget for the rendered size of the text, provided infinite
        # available space but a fixed number of lines
        fitting_size = self.native.textRectForBounds(
            NSMakeRect(0, 0, 100000, 100000),
            limitedToNumberOfLines=1,
        ).size

        self.interface.intrinsic.width = at_least(ceil(fitting_size.width))
        self.interface.intrinsic.height = at_least(ceil(fitting_size.height))
