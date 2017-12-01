from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super(PasswordInput, self).create()
        self.native.UseSystemPasswordChar = True
