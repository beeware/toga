from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super().create()
        self.native.UseSystemPasswordChar = True
