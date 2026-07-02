from .textinput import TextInput, TogaInput


class PasswordInput(TextInput):
    def create_native(self):
        return TogaInput(self, password=True)
