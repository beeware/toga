from toga_cocoa.libs import NSSecureTextField, NSTextFieldSquareBezel, objc_method


from .textinput import TextInput


class TogaSecureTextField(NSSecureTextField):
    @objc_method
    def textDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)


class PasswordInput(TextInput):
    def create(self):
        self.native = TogaSecureTextField.new()
        self.native.interface = self.interface

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

        # Add the layout constraints
        self.add_constraints()
