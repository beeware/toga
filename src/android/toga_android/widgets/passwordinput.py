from .textinput import TextInput, TogaTextInput


class PasswordInput(TextInput):
    def create(self):
        super(PasswordInput, self).create()
        self.native.inputType = 'textPassword'

