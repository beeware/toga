from ..libs import NSSecureTextField, NSTextFieldSquareBezel
from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        self.native = NSSecureTextField.new()
        self.native.interface = self.interface

        self.native.setBezeled_(True)
        self.native.setBezelStyle_(NSTextFieldSquareBezel)

        # Add the layout constraints
        self.add_constraints()
