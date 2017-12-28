from rubicon.objc import objc_method, SEL
from travertino.size import at_least

import toga
from toga.widgets.base import Widget as InterfaceWidget
from toga_cocoa.libs import NSStepper, NSObject

from .base import Widget
from .box import Box


class NumberInput(Box):
    def create(self):
        self.native = None
        self.constraints = None

        self.interface._children = []

        delegate = TextInputVerifier.alloc().init()
        delegate.controller = self

        self.text_input = toga.TextInput()
        self.text_input._impl.native.setDelegate_(delegate)
        self.interface.add(self.text_input)

        self.stepper = StepperInterface(
            min_value=self.interface._min_value,
            max_value=self.interface._max_value,
            step=self.interface._step
        )
        self.stepper.controller = self
        self.interface.add(self.stepper)
        self.set_value(self.interface._min_value)

        # self.interface.style.flex_direction = 'row'
        self.rehint()

    def text_update(self, handler):
        self.stepper.value = self.text_input.value

    def stepper_update(self):
        self.set_value(self.stepper.value)

    def set_value(self, value):
        self.stepper.value = value
        self.text_input.value = ('%f' % (value,)).rstrip('0').rstrip('.')

    def get_value(self):
        return self.text_input.value

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.text_input.style.height


class TextInputVerifier(NSObject):
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


class StepperInterface(InterfaceWidget):
    def __init__(self, id=None, style=None, factory=None,
                 min_value=0, max_value=100, step=1):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        super().__init__(id=id, style=style, factory=factory)
        self._impl = Stepper(interface=self)

    @property
    def value(self):
        return self._impl.native.floatValue

    @value.setter
    def value(self, val):
        self._impl.native.floatValue = float(val)

    def on_change(self, handler):
        self.controller.stepper_update()


class Stepper(Widget):
    def create(self):
        self.native = TogaStepper.alloc().init()
        self.native.interface = self.interface

        self.native.minValue = self.interface.min_value
        self.native.maxValue = self.interface.max_value
        self.native.increment = self.interface.step
        self.native.target = self.native
        self.native.action = SEL('onChange:')

        self.add_constraints()

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface._intrinsic.width = fitting_size.width
        self.interface._intrinsic.height = fitting_size.height
        # self.interface.style.margin_top = -3


class TogaStepper(NSStepper):
    @objc_method
    def onChange_(self, obj) -> None:
        process_callback(self.interface.on_change(self.interface))
