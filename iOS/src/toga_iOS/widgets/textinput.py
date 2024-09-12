from rubicon.objc import SEL, CGSize, objc_method, objc_property
from travertino.size import at_least

from toga.constants import LEFT, RIGHT
from toga_iOS.colors import native_color
from toga_iOS.libs import (
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTrailing,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSTextAlignment,
    UIColor,
    UIControlEventEditingChanged,
    UILabel,
    UITextBorderStyle,
    UITextField,
)
from toga_iOS.widgets.base import Widget


class TogaTextField(UITextField):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textFieldDidBeginEditing_(self, textField) -> None:
        self.interface.on_gain_focus()

    @objc_method
    def textFieldDidChange_(self, textField) -> None:
        self.interface._value_changed()

    @objc_method
    def textFieldDidEndEditing_(self, textField) -> None:
        self.interface.on_lose_focus()

    @objc_method
    def textFieldShouldReturn_(self, textField) -> bool:
        self.interface.on_confirm()
        return True


class TextInput(Widget):
    def create(self):
        self.native = TogaTextField.new()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        self.native.borderStyle = UITextBorderStyle.RoundedRect

        self.native.addTarget(
            self.native,
            action=SEL("textFieldDidChange:"),
            forControlEvents=UIControlEventEditingChanged,
        )

        # Add an (initially hidden) annotation to display errors
        self.add_error_label()

        # Add the layout constraints
        self.add_constraints()

    def add_error_label(self):
        # Provide an annotation in the view for error notifications
        self.error_label = UILabel.new()
        self.error_label.editable = False
        self.error_label.hidden = True

        self.error_label.translatesAutoresizingMaskIntoConstraints = False
        self.error_label.text = "\u26a0"  # Warning sign
        self.error_label.textColor = UIColor.redColor
        self.native.addSubview(self.error_label)

        leading_constraint = NSLayoutConstraint.constraintWithItem(
            self.native,
            attribute__1=NSLayoutAttributeLeading,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.error_label,
            attribute__2=NSLayoutAttributeLeading,
            multiplier=1.0,
            constant=8.0,
        )
        trailing_constraint = NSLayoutConstraint.constraintWithItem(
            self.native,
            attribute__1=NSLayoutAttributeTrailing,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.error_label,
            attribute__2=NSLayoutAttributeTrailing,
            multiplier=1.0,
            constant=8.0,
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

    def get_readonly(self):
        return not self.native.isEnabled()

    def set_readonly(self, value):
        self.native.enabled = not value

    def get_placeholder(self):
        # UIKit transparently converts "" into None
        return str(self.native.placeholder if self.native.placeholder else "")

    def set_placeholder(self, value):
        self.native.placeholder = value

    def get_value(self):
        return str(self.native.text)

    def set_value(self, value):
        self.native.text = value
        self.interface._value_changed()

    def set_alignment(self, value):
        self.native.textAlignment = NSTextAlignment(value)
        if value == RIGHT:
            self.error_label.textAlignment = NSTextAlignment(LEFT)
        else:
            self.error_label.textAlignment = NSTextAlignment(RIGHT)

    def set_color(self, color):
        self.native.textColor = native_color(color)

    def set_background_color(self, color):
        self.set_background_color_simple(color)

    def set_font(self, font):
        self.native.font = font._impl.native

    def rehint(self):
        # Height of a text input is known.
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = fitting_size.height

    def set_error(self, error_message):
        # Error message is currently unused.
        self.error_label.setHidden(False)

    def clear_error(self):
        self.error_label.setHidden(True)

    def is_valid(self):
        return self.error_label.isHidden()
