from tailor.platform.cocoa.libs import *
from .base import Widget


class TextInput(Widget):
    def __init__(self, value=None, placeholder=None, command=None):
        super(TextInput, self).__init__()

        self.command = command

        self._impl = NSTextField.new()

        self._impl.setEditable_(True)

        self._impl.setBezeled_(True)
        self._impl.setBezelStyle_(NSTextFieldSquareBezel)

    def value(self):
        return cfstring_to_string(self._impl.stringValue())
