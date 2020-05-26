import sys
from decimal import Decimal, InvalidOperation

from rubicon.objc import objc_method, SEL
from travertino.size import at_least

import toga
from toga_cocoa.libs import (
    NSTextAlignment, NSTextFieldSquareBezel, NSTextField, NSStepper,
    NSLayoutAttributeTop, NSLayoutAttributeBottom,
    NSLayoutAttributeLeft, NSLayoutAttributeRight,
    NSLayoutAttributeCenterY, NSLayoutRelationEqual, NSLayoutConstraint
)

from .base import Widget
from .box import TogaView


class TogaStepper(NSStepper):
    @objc_method
    def onChange_(self, stepper) -> None:
        self.interface.value = Decimal(stepper.floatValue).quantize(self.interface.step)
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    @objc_method
    def controlTextDidChange_(self, notification) -> None:
        try:
            value = str(self._impl.input.stringValue)
            # Try to convert to a decimal. If the value isn't a number,
            # this will raise InvalidOperation
            Decimal(value)
            # We set the input widget's value to the literal text input
            # This preserves the display of "123.", which Decimal will
            # convert to "123"
            self.interface.value = value
            if self.interface.on_change:
                self.interface.on_change(self.interface)
        except InvalidOperation:
            # If the string value isn't valid, reset the widget
            # to the widget's stored value. This will update the
            # display, removing any invalid values from view.
            self._impl.set_value(self.interface.value)


class NumberInput(Widget):
    def create(self):
        self.native = TogaView.alloc().init()

        self.input = NSTextField.new()
        self.input.interface = self.interface
        self.input.bezeled = True
        self.input.bezelStyle = NSTextFieldSquareBezel
        self.input.translatesAutoresizingMaskIntoConstraints = False

        self.stepper = TogaStepper.alloc().init()
        self.stepper.interface = self.interface
        self.stepper._impl = self
        self.stepper.translatesAutoresizingMaskIntoConstraints = False

        self.stepper.target = self.stepper
        self.stepper.action = SEL('onChange:')

        self.stepper.controller = self.input
        self.input.delegate = self.stepper

        # Add the input and stepper to the constraining box.
        self.native.addSubview(self.input)
        self.native.addSubview(self.stepper)

        # Add constraints to lay out the input and stepper.
        # Stepper is always top right corner.
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native, NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.stepper, NSLayoutAttributeTop,
                1.0, 0
            )
        )
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native, NSLayoutAttributeRight,
                NSLayoutRelationEqual,
                self.stepper, NSLayoutAttributeRight,
                1.0, 0
            )
        )

        # Stepper height matches container box height
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native, NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                self.stepper, NSLayoutAttributeBottom,
                1.0, 0
            )
        )

        # Input is always left, centred vertically on the stepper
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.stepper, NSLayoutAttributeCenterY,
                NSLayoutRelationEqual,
                self.input, NSLayoutAttributeCenterY,
                1.0, 0
            )
        )
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.native, NSLayoutAttributeLeft,
                NSLayoutRelationEqual,
                self.input, NSLayoutAttributeLeft,
                1.0, 0
            )
        )

        # Stepper and input meet in the middle with a small gap
        self.native.addConstraint(
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.stepper, NSLayoutAttributeLeft,
                NSLayoutRelationEqual,
                self.input, NSLayoutAttributeRight,
                1.0, 2
            )
        )

        # Add the layout constraints for the main box
        self.add_constraints()

    def set_readonly(self, value):
        # Even if it's not editable, it's still selectable.
        self.input.editable = not value
        self.input.selectable = True

    def set_placeholder(self, value):
        self.input.cell.placeholderString = value

    def set_step(self, step):
        self.stepper.increment = self.interface.step

    def set_min_value(self, value):
        if self.interface.min_value is None:
            self.stepper.minValue = -sys.maxsize
        else:
            self.stepper.minValue = value

    def set_max_value(self, value):
        if self.interface.max_value is None:
            self.stepper.maxValue = sys.maxsize
        else:
            self.stepper.maxValue = value

    def set_alignment(self, value):
        self.input.alignment = NSTextAlignment(value)

    def set_font(self, value):
        if value:
            self.input.font = value._impl.native

    def set_value(self, value):
        if self.interface.value is None:
            self.stepper.floatValue = 0
            self.input.stringValue = ''
        else:
            self.stepper.floatValue = float(self.interface.value)
            # We use the *literal* input value here, not the value
            # stored in the interface, because we want to display
            # what the user has actually input, not the interpreted
            # Decimal value. Any invalid input value should result
            # in the interface to a value of None, so this branch
            # should only execute if we know the raw value can be
            # converted to a Decimal.
            self.input.stringValue = value

    def rehint(self):
        # Height of a text input is known and fixed.
        stepper_size = self.input.intrinsicContentSize()
        input_size = self.input.intrinsicContentSize()

        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = max(input_size.height, stepper_size.height)

    def set_on_change(self, handler):
        # No special handling required
        pass
