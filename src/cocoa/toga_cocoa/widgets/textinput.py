from .base import Widget
from ..libs import NSTextField, NSTextFieldSquareBezel


class TextInput(Widget):
    _IMPL_CLASS = NSTextField

    def create(self):
        self.native = self._IMPL_CLASS.new()
        self.native.interface = self

        self.native.setBezeled_(True)
        self.native.setBezelStyle_(NSTextFieldSquareBezel)

        # Add the layout constraints
        self.add_constraints()

    def set_readonly(self, value):
        self.native.editable = not value

    def set_placeholder(self, value):
        self.native.cell.placeholderString = value

    def get_value(self):
        return self.native.stringValue

    def set_value(self, value):
        self.native.stringValue = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self._impl.fittingSize().width, self._impl.fittingSize().height)
        self.interface.style.hint(
            height=self.native.fittingSize().height,
            min_width=100
        )
