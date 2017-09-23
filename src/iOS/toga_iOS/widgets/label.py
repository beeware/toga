from toga.constants import LEFT_ALIGNED
from rubicon.objc import CGSize
from .base import Widget
from ..libs import UILabel, NSTextAlignment, NSLineBreakByWordWrapping, CGSize


class Label(Widget):
    def create(self):
        self.native = UILabel.new()
        self.native.interface = self

        self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self.native.setLineBreakMode_(NSLineBreakByWordWrapping)

        # Add the layout constraints
        self.add_constraints()

    def set_alignment(self, value):
        self.native.setTextAlignment_(NSTextAlignment(value))

    def set_text(self, value):
        self.native.setText_(value)

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            height=fitting_size.height,
            width=fitting_size.width
        )
