from toga_iOS.widgets.textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super().create()
        self.native.setSecureTextEntry(True)
