from __future__ import print_function, absolute_import, division

from ..libs import NSSecureTextField
from .textinput import TextInput


class PasswordInput(TextInput):
    _IMPL_CLASS = NSSecureTextField

    def __init__(self):
        super(PasswordInput, self).__init__()
