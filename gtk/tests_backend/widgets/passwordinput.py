from .textinput import TextInputProbe


class PasswordInputProbe(TextInputProbe):
    def __init__(self, widget):
        super().__init__(widget)

        assert not self.native.get_visibility()
