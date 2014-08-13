from __future__ import print_function, absolute_import, division

from ..libs import get_NSString, cfstring_to_string, NSTextField, NSTextFieldSquareBezel, text
from .base import Widget


class TextInput(Widget):
    _IMPL_CLASS = NSTextField

    def __init__(self, initial=None, placeholder=None, readonly=False):
        super(TextInput, self).__init__()

        self.startup()

        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial

    def startup(self):
        self._impl = self._IMPL_CLASS.new()

        self._impl.setBezeled_(True)
        self._impl.setBezelStyle_(NSTextFieldSquareBezel)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.setEditable_(not self._readonly)

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = value
        if value:
            self._impl.cell.setPlaceholderString_(get_NSString(self.placeholder))

    @property
    def value(self):
        return cfstring_to_string(self._impl.stringValue())

    @value.setter
    def value(self, value):
        if value:
            self._impl.setStringValue_(get_NSString(text(value)))
