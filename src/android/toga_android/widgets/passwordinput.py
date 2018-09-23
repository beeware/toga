from .textinput import TextInput, TogaTextInput


class PasswordInput(TextInput):
    def create(self):
        super().create()
        self.native.inputType = 'textPassword'

