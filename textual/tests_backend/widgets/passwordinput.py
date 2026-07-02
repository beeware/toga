from .textinput import TextInputProbe


class PasswordInputProbe(TextInputProbe):
    @property
    def value_hidden(self):
        return self.native.password
