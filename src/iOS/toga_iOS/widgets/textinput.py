from .base import Widget
from ..libs import UITextField, UITextBorderStyleRoundedRect
from rubicon.objc import CGSize


class TextInput(Widget):
    def create(self):
        self.native = UITextField.new()
        self.native._interface = self

        self.native.setBorderStyle_(UITextBorderStyleRoundedRect)

        # Add the layout constraints
        self.add_constraints()

    def set_readonly(self, value):
        self.native.enabled = not value

    def set_placeholder(self, value):
        self.native.placeholder = value

    def get_value(self):
        return self.native.text

    def set_value(self, value):
        self.native.text = value

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=100
        )
