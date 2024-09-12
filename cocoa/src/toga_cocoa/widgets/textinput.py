from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga.constants import LEFT, RIGHT
from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    SEL,
    NSColor,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTrailing,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSTextAlignment,
    NSTextField,
    NSTextFieldSquareBezel,
    NSTextView,
    c_void_p,
    objc_method,
    objc_property,
    send_super,
)

from .base import Widget


class TogaTextFieldProxy:
    # This is messy, but unfortunately inevitable. TextInput and PasswordInput
    # are *identical*, except for the Cocoa class that implements them. However,
    # we need to subclass the Cocoa class to provide key functionality - but
    # Rubicon doesn't allow for multiple base classes. So, we implement
    # subclassing by using a proxy - a class that holds all the actual
    # implementations as static methods that can be invoked passing in the
    # appropriate class/instance context from the "real" class.
    #
    # If you add a method to this proxy, make sure you add a hook to both the
    # TogaTextField and TogaSecureTextField implementations using the proxy.

    @staticmethod
    def textDidChange_(cls, self, notification) -> None:
        self.interface.on_change()
        self.interface._validate()

    @staticmethod
    def becomeFirstResponder(cls, self) -> bool:
        self.interface.on_gain_focus()
        return send_super(cls, self, "becomeFirstResponder")

    @staticmethod
    def textDidEndEditing_(cls, self, textObject) -> None:
        self.interface.on_lose_focus()
        send_super(cls, self, "textDidEndEditing:", textObject, argtypes=[c_void_p])

    @staticmethod
    def control_textView_doCommandBySelector_(
        cls,
        self,
        control,
        textView,
        selector: SEL,
    ) -> bool:
        if selector.name == b"insertNewline:":
            self.interface.on_confirm()
        return False


class TogaTextField(NSTextField):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textDidChange_(self, notification) -> None:
        TogaTextFieldProxy.textDidChange_(__class__, self, notification)

    @objc_method
    def becomeFirstResponder(self) -> bool:
        return TogaTextFieldProxy.becomeFirstResponder(__class__, self)

    @objc_method
    def textDidEndEditing_(self, textObject) -> None:
        TogaTextFieldProxy.textDidEndEditing_(__class__, self, textObject)

    @objc_method
    def control_textView_doCommandBySelector_(
        self,
        control,
        textView,
        selector: SEL,
    ) -> bool:
        return TogaTextFieldProxy.control_textView_doCommandBySelector_(
            __class__, self, control, textView, selector
        )


class TextInput(Widget):
    def create(self):
        self.native = self._make_instance()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        self.native.bezeled = True
        self.native.bezelStyle = NSTextFieldSquareBezel

        # Add an (initially hidden) annotation to display errors
        self.add_error_label()

        # Add the layout constraints
        self.add_constraints()

    def _make_instance(self):
        return TogaTextField.new()

    def add_error_label(self):
        # Provide an annotation in the view for error notifications
        self.error_label = NSTextField.alloc().init()
        self.error_label.drawsBackground = False
        self.error_label.editable = False
        self.error_label.bezeled = False
        self.error_label.hidden = True

        self.error_label.translatesAutoresizingMaskIntoConstraints = False
        self.error_label.stringValue = "\u26a0"  # Warning sign
        self.error_label.textColor = NSColor.systemRedColor
        self.native.addSubview(self.error_label)

        leading_constraint = NSLayoutConstraint.constraintWithItem(
            self.native,
            attribute__1=NSLayoutAttributeLeading,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.error_label,
            attribute__2=NSLayoutAttributeLeading,
            multiplier=1.0,
            constant=4.0,
        )
        trailing_constraint = NSLayoutConstraint.constraintWithItem(
            self.native,
            attribute__1=NSLayoutAttributeTrailing,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.error_label,
            attribute__2=NSLayoutAttributeTrailing,
            multiplier=1.0,
            constant=4.0,
        )
        center_y_constraint = NSLayoutConstraint.constraintWithItem(
            self.error_label,
            attribute__1=NSLayoutAttributeCenterY,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.native,
            attribute__2=NSLayoutAttributeCenterY,
            multiplier=1.0,
            constant=0.0,
        )
        self.native.addConstraints(
            [
                leading_constraint,
                trailing_constraint,
                center_y_constraint,
            ]
        )

    @property
    def has_focus(self):
        # When the NSTextField gets focus, a field editor is created, and that editor
        # has the original widget as the delegate. The first responder is the Field Editor.
        return (
            self.native.window is not None
            and isinstance(self.native.window.firstResponder, NSTextView)
            and self.native.window.firstResponder.delegate == self.native
        )

    def get_readonly(self):
        return not self.native.isEditable()

    def set_readonly(self, value):
        # Even if it's not editable, it's still selectable.
        self.native.editable = not value
        self.native.selectable = True

    def get_placeholder(self):
        return str(self.native.cell.placeholderString)

    def set_placeholder(self, value):
        self.native.cell.placeholderString = value

    def set_alignment(self, value):
        self.native.alignment = NSTextAlignment(value)
        # The alert label should be on the trailing edge
        if value == RIGHT:
            self.error_label.alignment = NSTextAlignment(LEFT)
        else:
            self.error_label.alignment = NSTextAlignment(RIGHT)

    def set_font(self, font):
        self.native.font = font._impl.native
        self.error_label.font = font._impl.native

    def set_color(self, color):
        self.native.textColor = native_color(color)

    def set_background_color(self, color):
        if color is TRANSPARENT:
            # The text view needs to be made transparent *and* non-bezeled
            self.native.drawsBackground = False
            self.native.bezeled = False
        else:
            self.native.drawsBackground = True
            self.native.bezeled = True
            self.native.backgroundColor = native_color(color)

    def get_value(self):
        return str(self.native.stringValue)

    def set_value(self, value):
        self.native.stringValue = value
        self.interface._value_changed()

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self,
        #     self._impl.intrinsicContentSize().width, self._impl.intrinsicContentSize().height
        # )
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = self.native.intrinsicContentSize().height

    def set_error(self, error_message):
        self.error_label.toolTip = error_message
        self.error_label.hidden = False

    def clear_error(self):
        self.error_label.hidden = True

    def is_valid(self):
        return self.error_label.isHidden()
