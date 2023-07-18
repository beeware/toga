from toga.fonts import SYSTEM

from .textinput import TextInputProbe


class PasswordInputProbe(TextInputProbe):
    # In password mode, the EditText defaults to monospace.
    def assert_font_family(self, expected):
        actual = self.font.family
        if expected == SYSTEM:
            assert actual == "monospace"
        else:
            assert actual == expected
