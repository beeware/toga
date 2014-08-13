from __future__ import print_function, absolute_import, division

from ..libs import get_NSString, cfstring_to_string, UITextField, UITextBorderStyleRoundedRect, text
from .base import Widget


class TextInput(Widget):
    def __init__(self, initial=None, placeholder=None, readonly=False):
        super(TextInput, self).__init__()
        self.placeholder = placeholder

        self.startup()

        self.value = initial
        # self.readonly = readonly

    def startup(self):
        self._impl = UITextField.new()
        if self.placeholder:
            self._impl.setPlaceholder_(get_NSString(self.placeholder))

        self._impl.setBorderStyle_(UITextBorderStyleRoundedRect)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.setEditable_(not self._readonly)

    @property
    def value(self):
        return cfstring_to_string(self._impl.text)

    @value.setter
    def value(self, value):
        if value:
            self._impl.setText_(get_NSString(text(value)))
