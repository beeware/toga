from rubicon.objc import objc_method, get_selector

from toga.interface import NumberInput as NumberInputInterface
from toga.interface import Widget

from .textinput import TextInput
from .box import Box
from .base import WidgetMixin

from ..libs import NSStepper
from ..utils import process_callback
from ..container import Constraints



class TogaStepper(NSStepper):

    @objc_method
    def onChange_(self, obj) -> None:
        process_callback(self._interface.on_change(self.interface))


class Stepper(WidgetMixin, Widget):

    def __init__(self, id=None, style=None, min=0, max=100, step=1):
        super().__init__(id=id, style=style, min=min, max=max, step=step)
        self._create()

    def _configure(self, **kw):
        pass

    def create(self):

        self._impl = TogaStepper.alloc().init()
        self._impl.interface = self
        self._impl.minValue = self._config["min"]
        self._impl.maxValue = self._config["max"]
        self._impl.increment = self._config["step"]

        self._add_constraints()

    def rehint(self):
        self.style.hint(
            height=self._impl.fittingSize().height,
            min_width=self._impl.fittingSize().width
        )



class NumberInput(Box, NumberInputInterface):

    def __init__(self, id=None, style=None, min=0, max=100, step=1, children=None):
        super().__init__(id=id, style=style, children=children)
        self._config["min"] = min
        self._config["max"] = max
        self._config["step"] = step

    def _configure(self, **kw):
        pass

    def create(self):

        self._text = TextInput()
        self.add(self._text)

        self._stepper = Stepper(None, None, self._config["min"], self._config["max"], self._config["step"])
        self.add(self._stepper)

        self._constraints = Constraints(self)

        self.style.flex_direction = 'row'

    def _set_value(self, value):
        pass

    def rehint(self):
        self._text.rehint()
        self._stepper.rehint()

        self._stepper._impl.fittingSize().width + self._text._impl.fittingSize().width
