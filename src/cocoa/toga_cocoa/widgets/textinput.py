from travertino.size import at_least

from toga_cocoa.libs import (
    NSObject,
    NSTextAlignment,
    NSTextField,
    NSTextFieldSquareBezel,
    objc_method,
    NSColor,
)

from .base import Widget


class TogaTextFieldDelegate(NSObject):
    @objc_method
    def controlTextDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)
        self.interface.validate()


class TextInput(Widget):
    def create(self):
        self.native = NSTextField.new()
        self.native.interface = self.interface

        delegate = TogaTextFieldDelegate.new()
        delegate.interface = self.interface
        self.native.delegate = delegate

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
        self.native.wantsLayer = True
        self.native.layer.borderColor = NSColor.redColor.CGColor
        self.native.layer.borderWidth = 1.0
        self.native.layer.cornerRadius = 0.0
        self.native.toolTip = error_message

    def unset_error(self):
        self.set_background_color(None)
        self.native.toolTip = ""
        if self.native.layer is not None:
            self.native.layer.borderColor = None
        self.native.wantsLayer = False
