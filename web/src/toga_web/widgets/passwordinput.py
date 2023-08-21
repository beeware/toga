from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super().create()
        self.native.setAttribute("type", "password")

    def is_valid(self):
        self.interface.factory.not_implemented("PasswordInput.is_valid()")
        return True
