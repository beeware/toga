from __future__ import print_function, absolute_import, division, unicode_literals

from ..libs import NSSecureTextField
from .textinput import TextInput


class PasswordInput(TextInput):
    _IMPL_CLASS = NSSecureTextField

    def __init__(self, **style):
        super(PasswordInput, self).__init__(**style)
