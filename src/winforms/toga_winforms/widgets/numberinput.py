from ..libs import WinForms, ClrDecimal

from toga.interface import NumberInput as NumberInputInterface

from .base import WidgetMixin


class NumberInput(WidgetMixin, NumberInputInterface):
    _IMPL_CLASS = WinForms.NumericUpDown

    def __init__(self, id=None, style=None, min_value=0, max_value=100, step=1,
                 **ex):
        super().__init__(id=id, style=style, min_value=min_value,
                         max_value=max_value, step=step, **ex)
        self._create()

    def create(self):
        self._impl = self._IMPL_CLASS()
        self._impl._interface = self
        self.rehint()

    def _get_value(self):
        return self._impl.Value

    def _set_value(self, value):
        if value is not None and value is not "":
            self._impl.Value = ClrDecimal.Parse(value)

    def rehint(self):
        self.style.min_width = 120
        self.style.height = 32
