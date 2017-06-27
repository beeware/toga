from .base import Widget
from ..libs import NSTextField, NSTextFieldSquareBezel


class TextInput(Widget):
    _IMPL_CLASS = NSTextField

    def create(self):
        self._native = self._IMPL_CLASS.new()
        self._native._interface = self

        self._native.setBezeled_(True)
        self._native.setBezelStyle_(NSTextFieldSquareBezel)

        # Add the layout constraints
        self.add_constraints()

    def set_readonly(self, value):
        self._native.editable = not value

    def set_placeholder(self, value):
        self._native.cell.placeholderString = value

    def get_value(self):
        return self._native.stringValue

    def set_value(self, value):
        self._native.stringValue = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self._impl.fittingSize().width, self._impl.fittingSize().height)
        self._interface.style.hint(
            height=self._native.fittingSize().height,
            min_width=100
        )
