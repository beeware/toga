from toga_cocoa.libs import NSSecureTextField, NSTextFieldSquareBezel

from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        self.native = NSSecureTextField.new()
        self.native.interface = self.interface

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

        # Add the layout constraints
        self.add_constraints()
