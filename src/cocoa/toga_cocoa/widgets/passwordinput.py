from toga_cocoa.libs import NSSecureTextField, NSTextFieldSquareBezel

from .textinput import TextInput, TogaTextFieldDelegate


class PasswordInput(TextInput):
    def create(self):
        self.native = NSSecureTextField.new()
        self.native.interface = self.interface

        delegate = TogaTextFieldDelegate.new()
        delegate.interface = self.interface
        self.native.delegate = delegate

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

        # Add the layout constraints
        self.add_constraints()
