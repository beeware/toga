from math import ceil

from rubicon.objc import CGSize
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_iOS.colors import native_color
from toga_iOS.libs import NSLineBreakByWordWrapping, NSTextAlignment, UILabel
from toga_iOS.widgets.base import Widget


class Label(Widget):
    def create(self):
        self.native = UILabel.new()
        # Word wrap the text inside the allocated space
        self.native.lineBreakMode = NSLineBreakByWordWrapping

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
        return self.native.text

    def set_text(self, value):
        self.native.text = value
        # Tell the text layout algorithm how many lines are allowed
        self.native.numberOfLines = len(self.interface.text.split("\n"))

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        # print("REHINT label", self, fitting_size.width, fitting_size.height)
        self.interface.intrinsic.width = at_least(ceil(fitting_size.width))
        self.interface.intrinsic.height = ceil(fitting_size.height)
