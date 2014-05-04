from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget


class PasswordInput(Widget):
    def __init__(self, value=None, placeholder=None, command=None):
        super(PasswordInput, self).__init__()

        self.command = command

        self._impl = NSSecureTextField.new()

        self._impl.setEditable_(True)

        self._impl.setBezeled_(True)
        self._impl.setBezelStyle_(NSTextFieldSquareBezel)

    def value(self):
        return cfstring_to_string(self._impl.stringValue())
