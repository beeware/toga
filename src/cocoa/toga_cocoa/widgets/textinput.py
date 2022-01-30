from travertino.size import at_least

from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    NSColor,
    NSTextAlignment,
    NSTextField,
    NSTextFieldSquareBezel,
    c_void_p,
    objc_method,
    send_super,
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

    @objc_method
    def becomeFirstResponder(self) -> bool:
        # Cocoa gives and then immediately revokes focus when the widget
        # is first displayed. Set a local attribute on the first *loss*
        # of focus, and only trigger Toga events when that attribute exists.
        if hasattr(self, '_configured'):
            if self.interface.on_gain_focus:
                self.interface.on_gain_focus(self.interface)
        return send_super(__class__, self, 'becomeFirstResponder')

    @objc_method
    def textDidEndEditing_(self, textObject) -> None:
        # Cocoa gives and then immediately revokes focus when the widget
        # is first displayed. Set a local attribute on the first *loss*
        # of focus, and only trigger Toga events when that attribute exists.
        if hasattr(self, '_configured'):
            if self.interface.on_lose_focus:
                self.interface.on_lose_focus(self.interface)
        else:
            self._configured = True

        send_super(__class__, self, 'textDidEndEditing:', textObject, argtypes=[c_void_p])


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

    def set_color(self, color):
        if color:
            self.native.textColor = native_color(color)
        else:
            self.native.textColor = NSColor.labelColor

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

    def set_on_gain_focus(self, handler):
        pass

    def set_on_lose_focus(self, handler):
        pass

    def set_error(self, error_message):
        if self.interface.window is not None:
            self.interface.window.error_dialog("Validation Error", error_message)

    def clear_error(self):
        # Cocoa TextInput can't ever be in an invalid state, so clear is a no-op
        pass
