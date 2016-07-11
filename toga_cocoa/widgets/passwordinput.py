from ..libs import NSSecureTextField
from .textinput import TextInput


class PasswordInput(TextInput):
    _IMPL_CLASS = NSSecureTextField

    def __init__(self, style=None):
        super(PasswordInput, self).__init__(style=style)
