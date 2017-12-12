from toga_cocoa.libs import NSTextField, NSTextFieldSquareBezel

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = NSTextField.new()
        self.native.interface = self.interface

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

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
