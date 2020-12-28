from .textinput import TextInput


class PasswordInput(TextInput):
    """This widget behaves like a TextInput, but obscures the text that is
    entered by the user.
    """
    def _create(self):
        self._impl = self.factory.PasswordInput(interface=self)

    def set_font(self, font):
        raise AttributeError("PasswordInput.set_font is non-sensical.")
