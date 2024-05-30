import sys
from decimal import Decimal, InvalidOperation

from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga.widgets.numberinput import _clean_decimal, _clean_decimal_str
from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutAttributeTop,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSStepper,
    NSTextAlignment,
    NSTextField,
    NSTextFieldSquareBezel,
    NSTextView,
    NSView,
)

from .base import Widget


class TogaStepper(NSStepper):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onChange_(self, stepper) -> None:
        # Stepper has increased/decreased
        self.interface.value = _clean_decimal(stepper.floatValue, self.interface.step)

    @objc_method
    def controlTextDidChange_(self, notification) -> None:
        value = str(self.impl.native_input.stringValue)
        try:
            # Try to convert to a decimal. If the value isn't a number,
            # this will raise InvalidOperation
            Decimal(value)
        except InvalidOperation:
            # If the string value isn't valid, remove any characters that
            # would make it invalid.
            self.impl.native_input.stringValue = _clean_decimal_str(value)

        self.interface.on_change()


class TogaNumberInput(NSTextField):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textDidEndEditing_(self, notification) -> None:
        # Loss of focus; ensure that the displayed value
        # matches the clipped, normalized decimal value
        self.impl.set_value(self.interface.value)


class NumberInput(Widget):
    def create(self):
        self.native = NSView.alloc().init()

        self.native_input = TogaNumberInput.new()
        self.native_input.interface = self.interface
        self.native_input.impl = self
        self.native_input.bezeled = True
        self.native_input.bezelStyle = NSTextFieldSquareBezel
        self.native_input.translatesAutoresizingMaskIntoConstraints = False
        self.native_input.selectable = True

        self.native_stepper = TogaStepper.alloc().init()
        self.native_stepper.interface = self.interface
        self.native_stepper.impl = self
        self.native_stepper.translatesAutoresizingMaskIntoConstraints = False

        self.native_stepper.target = self.native_stepper
        self.native_stepper.action = SEL("onChange:")

        self.native_stepper.valueWraps = False

        self.native_stepper.controller = self.native_input
        self.native_input.delegate = self.native_stepper

        # Add the input and stepper to the constraining box.
        self.native.addSubview(self.native_input)
        self.native.addSubview(self.native_stepper)

        # Add constraints to lay out the input and stepper.
        # Stepper is always top right corner.
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.native_stepper,
                NSLayoutAttributeTop,
                1.0,
                0,
            )
        )
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native,
                NSLayoutAttributeRight,
                NSLayoutRelationEqual,
                self.native_stepper,
                NSLayoutAttributeRight,
                1.0,
                0,
            )
        )

        # Stepper height matches container box height
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native,
                NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                self.native_stepper,
                NSLayoutAttributeBottom,
                1.0,
                0,
            )
        )

        # Input is always left, centred vertically on the stepper
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native_stepper,
                NSLayoutAttributeCenterY,
                NSLayoutRelationEqual,
                self.native_input,
                NSLayoutAttributeCenterY,
                1.0,
                0,
            )
        )
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native,
                NSLayoutAttributeLeft,
                NSLayoutRelationEqual,
                self.native_input,
                NSLayoutAttributeLeft,
                1.0,
                0,
            )
        )

        # Stepper and input meet in the middle with a small gap
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native_stepper,
                NSLayoutAttributeLeft,
                NSLayoutRelationEqual,
                self.native_input,
                NSLayoutAttributeRight,
                1.0,
                2,
            )
        )

        # Add the layout constraints for the main box
        self.add_constraints()

    def set_color(self, color):
        self.native_input.textColor = native_color(color)

    def set_background_color(self, color):
        if color is TRANSPARENT:
            # The text view needs to be made transparent *and* non-bezeled
            self.native_input.drawsBackground = False
            self.native_input.bezeled = False
        else:
            self.native_input.drawsBackground = True
            self.native_input.bezeled = True
            self.native_input.backgroundColor = native_color(color)

    def has_focus(self):
        # When the NSTextField gets focus, a field editor is created, and that editor
        # has the original widget as the delegate. The first responder is the Field Editor.
        return isinstance(self.native.window.firstResponder, NSTextView) and (
            self.native.window.firstResponder.delegate == self.native_input
        )

    def focus(self):
        if not self.has_focus():
            self.interface.window._impl.native.makeFirstResponder(self.native_input)

    def get_readonly(self):
        return not self.native_input.isEditable()

    def set_readonly(self, value):
        self.native_input.editable = not value

    def set_step(self, step):
        self.native_stepper.increment = step

    def set_min_value(self, value):
        if value is None:
            self.native_stepper.minValue = -sys.float_info.max
        else:
            self.native_stepper.minValue = float(value)

    def set_max_value(self, value):
        if value is None:
            self.native_stepper.maxValue = sys.float_info.max
        else:
            self.native_stepper.maxValue = float(value)

    def set_alignment(self, value):
        self.native_input.alignment = NSTextAlignment(value)

    def set_font(self, font):
        self.native_input.font = font._impl.native

    def get_value(self):
        try:
            return _clean_decimal(
                str(self.native_input.stringValue), self.interface.step
            )
        except InvalidOperation:
            return None

    def set_value(self, value):
        if value is None:
            self.native_stepper.floatValue = 0.0
            self.native_input.stringValue = ""
        else:
            self.native_stepper.floatValue = float(value)
            self.native_input.stringValue = str(value)
        self.interface.on_change()

    def get_enabled(self):
        return self.native_input.isEnabled

    def set_enabled(self, value):
        self.native_input.enabled = value
        self.native_stepper.enabled = value

    def rehint(self):
        # Height of a text input is known and fixed.
        input_size = self.native_input.intrinsicContentSize()
        stepper_size = self.native_stepper.intrinsicContentSize()

        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = max(input_size.height, stepper_size.height)
