from rubicon.objc import objc_method, get_selector

from toga.interface import NumberInput as NumberInputInterface
from toga.interface import Widget

from .textinput import TextInput
from .box import Box
from .base import WidgetMixin

from ..libs import NSStepper, NSView, NSMakeRect, NSObject
from ..utils import process_callback
from ..container import Constraints



class TextInputVerifier(NSObject):

    @objc_method
    def textShouldEndEditing_(self, text) -> int:
        print('should end')
        return 0

    @objc_method
    def textDidEndEditing_(self, notification) -> None:
        print('d')
        self._controller._text_update()


class TogaStepper(NSStepper):

    @objc_method
    def onChange_(self, obj) -> None:
        if self._interface.on_change:
            process_callback(self._interface.on_change(self._interface))


class Stepper(WidgetMixin, Widget):

    def __init__(self, controller, id=None, style=None, min=0, max=100, step=1):
        super().__init__(id=id, style=style, min=min, max=max, step=step)
        self._create()
        self.controller = controller

    def _configure(self, **kw):
        pass

    @property
    def value(self):
        return self._impl.floatValue

    @value.setter
    def value(self, val):
        self._impl.floatValue = val

    def on_change(self, handler):
        self.controller._stepper_update()

    def create(self):

        self._impl = TogaStepper.alloc().init()
        self._impl._interface = self

        self._impl.minValue = self._config["min"]
        self._impl.maxValue = self._config["max"]
        self._impl.increment = self._config["step"]
        self._impl.setTarget_(self._impl)
        self._impl.setAction_(get_selector('onChange:'))

        self._add_constraints()

    def rehint(self):
        self.style.hint(
            height=self._impl.fittingSize().height,
            min_width=self._impl.fittingSize().width
        )
        self.style.margin_top = -3



class NumberInput(Box, NumberInputInterface):

    def __init__(self, id=None, style=None, min=0, max=100, step=1, children=None):
        super().__init__(id=id, style=style, children=children)
        self._config["min"] = min
        self._config["max"] = max
        self._config["step"] = step

    def _configure(self, **kw):
        pass

    def _text_update(self):
        self._stepper.value = self._text.value

    def _stepper_update(self):
        self._text.value = self._stepper.value

    def create(self):

        self._impl = NSView.alloc().init(NSMakeRect(0,0,100,100))
        self._add_constraints()

        delegate = TextInputVerifier.alloc().init()
        delegate._controller = self
        self._text = TextInput(_delegate=delegate)
        self.add(self._text)

        self._stepper = Stepper(
            self, min=self._config["min"], max=self._config["max"],
            step=self._config["step"])
        self.add(self._stepper)

        self.style.flex_direction = 'row'
        self.rehint()

    def _set_value(self, value):
        self._stepper.value = value
        self._text.value = value

    def rehint(self):
        self._text.rehint()
        self._stepper.rehint()

        self.style.hint(
            height=self._text.style.height,
            min_width=120,
        )
