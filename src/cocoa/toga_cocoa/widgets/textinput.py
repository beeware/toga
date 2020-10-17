from travertino.size import at_least

from toga_cocoa.libs import (
    NSTextAlignment,
    NSTextField,
    NSTextFieldSquareBezel,
    objc_method,
)

from .base import Widget


class TogaTextField(NSTextField):
    @objc_method
    def textDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    @objc_method
    def textShouldEndEditing_(self, textObject) -> bool:
        return self.interface.validate()


class TextInput(Widget):
    def create(self):
        self.native = TogaTextField.new()
        self.native.interface = self.interface

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

        # Add the layout constraints
        self.add_constraints()

    def set_readonly(self, value):
        # Even if it's not editable, it's still selectable.
        self.native.editable = not value
        self.native.selectable = True

    def set_placeholder(self, value):
        self.native.cell.placeholderString = value

    def set_alignment(self, value):
        self.native.alignment = NSTextAlignment(value)

    def set_font(self, font):
        if font:
            self.native.font = font.bind(self.interface.factory).native

    def get_value(self):
        return str(self.native.stringValue)

    def set_value(self, value):
        self.native.stringValue = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self,
        #     self._impl.intrinsicContentSize().width, self._impl.intrinsicContentSize().height
        # )
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.intrinsicContentSize().height

    def set_on_change(self, handler):
        pass

    def set_error(self, error_message):
        if self.interface.window is not None:
            self.interface.window.error_dialog("Validation Error", error_message)

    def clear_error(self):
        # Cocoa TextInput can't ever be in an invalid state, so clear is a no-op
        pass
