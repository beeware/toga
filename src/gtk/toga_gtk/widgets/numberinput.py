from gi.repository import Gtk

from toga.interface import NumberInput as NumberInputInterface

from .base import WidgetMixin

class NumberInput(WidgetMixin, NumberInputInterface):

    def __init__(self, id=None, style=None, min_value=0, max_value=100, step=1,
                 **ex):
        super().__init__(id=id, style=style, min_value=min_value,
                         max_value=max_value, step=step, **ex)
        self._create()

    def create(self):
        adjustment = Gtk.Adjustment(0, self._min_value, self._max_value,
                                    self._step, 10, 0)

        self._impl = Gtk.SpinButton()
        self._impl.set_adjustment(adjustment)
        self._impl.set_numeric(True)
        self._impl._interface = self

        self.rehint()

    def _get_value(self):
        return self._impl.get_value()

    def _set_value(self, value):
        self._impl.set_value(value)

    def rehint(self):
        self.style.min_width = 120
        self.style.height = 32
