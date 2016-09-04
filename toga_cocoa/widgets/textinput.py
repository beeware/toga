from rubicon.objc import text

from ..libs import NSTextField, NSTextFieldSquareBezel
from .base import Widget


class TextInput(Widget):
    _IMPL_CLASS = NSTextField

    def __init__(self, initial=None, placeholder=None, readonly=False, style=None):
        super(TextInput, self).__init__(style=style)

        self.startup()

        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial

    def startup(self):
        self._impl = self._IMPL_CLASS.new()
        self._impl._interface = self

        self._impl.setBezeled_(True)
        self._impl.setBezelStyle_(NSTextFieldSquareBezel)

        # Height of a text input is known and fixed.
        # Width must be > 100
        self.style.hint(
            height=self._impl.fittingSize().height,
            width=(100, None)
        )

        # Add the layout constraints
        self._add_constraints()

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
            self._impl.cell.setPlaceholderString_(self.placeholder)

    @property
    def value(self):
        return self._impl.stringValue

    @value.setter
    def value(self, value):
        if value:
            self._impl.stringValue = text(value)
