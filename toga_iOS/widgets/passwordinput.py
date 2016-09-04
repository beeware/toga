from .textinput import TextInput


class PasswordInput(TextInput):
    def __init__(self, placeholder=None, style=None):
        super().__init__(placeholder=placeholder, style=style)

    def startup(self):
        super().startup()
        self._impl.setSecureTextEntry_(True)
