from __future__ import print_function, absolute_import, division

from .textinput import TextInput


class PasswordInput(TextInput):
    def create(self):
        super(PasswordInput, self).create()
        self.native.UseSystemPasswordChar = True
