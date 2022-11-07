from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        self._action("create PasswordInput")
