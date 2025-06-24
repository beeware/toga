from math import ceil

from rubicon.objc import CGRect, NSInteger, NSMakeRect, objc_method, send_super
from travertino.size import at_least

from toga_iOS.colors import native_color
from toga_iOS.libs import (
    NSLineBreakByClipping,
    NSTextAlignment,
    UILabel,
)
from toga_iOS.widgets.base import Widget


class TogaLabel(UILabel):
    @objc_method
    def drawTextInRect_(self, rect: CGRect) -> None:
        # Evaluate the size of the rectangle needed to actually render the text
        minimal_rect = send_super(
            __class__,
            self,
            "textRectForBounds:limitedToNumberOfLines:",
            self.bounds,
            self.numberOfLines,
            restype=CGRect,
            argtypes=[CGRect, NSInteger],
        )
        # Draw using the minimal rectangle. As this has the minimum height,
        # drawn at the origin, it results in the text being drawn at the top
        # of the available rectangle.
        send_super(__class__, self, "drawTextInRect:", minimal_rect, argtypes=[CGRect])


class Label(Widget):
    def create(self):
        self.native = TogaLabel.new()
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

    def get_text(self):
        value = str(self.native.text)
        if value == "\u200b":
            return ""
        return value

    def set_text(self, value):
        if value == "":
            value = "\u200b"
        self.native.text = value
        # Tell the text layout algorithm how many lines are allowed
        self.native.numberOfLines = len(self.interface.text.split("\n"))

    def rehint(self):
        # Ask the widget for the rendered size of the text, provided infinite
        # available space but a fixed number of lines
        fitting_size = self.native.textRectForBounds(
            NSMakeRect(0, 0, 100000, 100000),
            limitedToNumberOfLines=len(self.interface.text.split("\n")),
        ).size

        # print(
        #     f"REHINT label {self} {self.get_text()!r} "
        #     f"{fitting_size.width} {fitting_size.height}"
        # )
        self.interface.intrinsic.width = at_least(ceil(fitting_size.width))
        self.interface.intrinsic.height = ceil(fitting_size.height)
