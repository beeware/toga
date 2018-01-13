from rubicon.objc import objc_method, SEL
from travertino.size import at_least

import toga
from toga_cocoa.libs import NSTextAlignment, NSTextFieldSquareBezel, NSTextField, NSObject

from .base import Widget


class TogaNumberFieldDelegate(NSObject):
    @objc_method
    def controlTextDidChange_(self, notification) -> None:
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    @objc_method
    def control_textShouldEndEditing_(self, text) -> int:
        try:
            float(text.stringValue)
            return 1
        except Exception as e:
            return 0

    @objc_method
    def controlTextDidEndEditing_(self, notification) -> None:
        if self.controller.text_update:
            self.controller.text_update(self.controller)


class NumberInput(Widget):
    def create(self):
        self.native = NSTextField.new()
        self.native.interface = self.interface

        delegate = TogaNumberFieldDelegate.new()
        delegate.interface = self.interface
        delegate.controller = self.native
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

    def set_font(self, value):
        if value:
            self.native.font = value._impl.native

    def get_value(self):
        return self.native.stringValue

    def set_value(self, value):
        self.native.stringValue = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self._impl.fittingSize().width, self._impl.fittingSize().height)
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.fittingSize().height

    def set_on_change(self, handler):
        pass


# class StepperInterface(InterfaceWidget):
#     def __init__(self, id=None, style=None, factory=None,
#                  min_value=0, max_value=100, step=1):
#         self.min_value = min_value
#         self.max_value = max_value
#         self.step = step
#         super().__init__(id=id, style=style, factory=factory)
#         self._impl = Stepper(interface=self)

#     @property
#     def value(self):
#         return self._impl.native.floatValue

#     @value.setter
#     def value(self, val):
#         self._impl.native.floatValue = float(val)

#     def on_change(self, handler):
#         self.controller.stepper_update()


# class TogaStepper(NSStepper):
#     @objc_method
#     def onChange_(self, obj) -> None:
#         process_callback(self.interface.on_change(self.interface))


# class Stepper(Widget):
#     def create(self):
#         self.native = TogaStepper.alloc().init()
#         self.native.interface = self.interface

#         self.native.minValue = self.interface.min_value
#         self.native.maxValue = self.interface.max_value
#         self.native.increment = self.interface.step
#         self.native.target = self.native
#         self.native.action = SEL('onChange:')

#         self.add_constraints()

#     def rehint(self):
#         fitting_size = self.native.fittingSize()
#         self.interface._intrinsic.width = fitting_size.width
#         self.interface._intrinsic.height = fitting_size.height
#         # self.interface.style.margin_top = -3
