from toga.interface import NumberInput as NumberInputInterface

from .base import WidgetMixin

from ..libs import NSStepper

class NumberInput(WidgetMixin, NumberInputInterface):

    def __init__(self, id=None, style=None, min=0, max=100, step=1):
        super().__init__(id=id, style=style, min=min, max=max, step=step)
        self._create()

    def create(self):

        self._impl = NSStepper.alloc().init()
        self._impl.minValue = self._config["min"]
        self._impl.maxValue = self._config["max"]
        self._impl.increment = self._config["step"]


        # Add the layout constraints
        self._add_constraints()

    def _set_value(self, value):
        pass

    def rehint(self):
        fitting_size = self._impl.fittingSize()
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
