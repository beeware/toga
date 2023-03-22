from math import ceil

from rubicon.objc import CGSize
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_iOS.colors import native_color
from toga_iOS.libs import NSLineBreakByClipping, NSTextAlignment, UILabel
from toga_iOS.widgets.base import Widget


class Label(Widget):
    def create(self):
        self.native = UILabel.new()
        # We shouldn't ever word wrap; if faced with that option, clip.
        self.native.lineBreakMode = NSLineBreakByClipping

        # Add the layout constraints
        self.add_constraints()

    def set_alignment(self, value):
        self.native.textAlignment = NSTextAlignment(value)

    def set_color(self, value):
        self.native.textColor = native_color(value)

    def set_background_color(self, color):
        if color == TRANSPARENT or color is None:
            self.native.backgroundColor = native_color(TRANSPARENT)
        else:
            self.native.backgroundColor = native_color(color)

    def set_font(self, font):
        self.native.font = font._impl.native

    def get_text(self):
        value = str(self.native.text)
        if value == "\u200B":
            return ""
        return value

    def set_text(self, value):
        if value == "":
            value = "\u200B"
        self.native.text = value
        # Tell the text layout algorithm how many lines are allowed
        self.native.numberOfLines = len(self.interface.text.split("\n"))

    def rehint(self):
        # iOS text layout is an interplay between the layout constraints and the
        # text layout algorithm. If the layout constraints fix the width, this
        # can cause the text layout algorithm to try word wrapping to make text
        # fit. To avoid this, temporarily relax the width and height constraint
        # on the widget to "effectively infinite" values; they will be
        # re-applied as part of the application of the newly hinted layout.
        if self.constraints:
            if self.constraints.width_constraint:
                self.constraints.width_constraint.constant = 100000
            if self.constraints.height_constraint:
                self.constraints.height_constraint.constant = 100000
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        # print(f"REHINT label {self} {self.get_text()!r} {fitting_size.width} {fitting_size.height}")
        self.interface.intrinsic.width = at_least(ceil(fitting_size.width))
        self.interface.intrinsic.height = ceil(fitting_size.height)
