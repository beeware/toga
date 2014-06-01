from __future__ import print_function, absolute_import, division

from ..libs import get_NSString, cfstring_to_string, UITextField, UITextBorderStyleRoundedRect
from .base import Widget


class TextInput(Widget):
    def __init__(self, initial=None, placeholder=None):
        super(TextInput, self).__init__()
        self.initial = initial
        self.placeholder = placeholder

    def _startup(self):
        self._impl = UITextField.new()
        if self.initial:
            self._impl.setText_(get_NSString(self.initial))
        if self.placeholder:
            self._impl.setPlaceholder_(get_NSString(self.placeholder))

        # self._impl.setEditable_(True)
        self._impl.setBorderStyle_(UITextBorderStyleRoundedRect)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    def value(self):
        return cfstring_to_string(self._impl.text)
