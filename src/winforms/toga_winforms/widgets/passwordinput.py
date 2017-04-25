from __future__ import print_function, absolute_import, division

from .textinput import TextInput


class PasswordInput(TextInput):
    def __init__(self):
        super(PasswordInput, self).__init__()

    def create(self):
        super(PasswordInput, self).create()
        self._impl.UseSystemPasswordChar = True
