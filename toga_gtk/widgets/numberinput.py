from gi.repository import Gtk

from toga.interface import NumberInput as NumberInputInterface

from .base import WidgetMixin

class NumberInput(WidgetMixin, NumberInputInterface):

    def __init__(self, id=None, style=None, min=0, max=100, step=1, **ex):
        super().__init__(id=id, style=style, min=min, max=max, step=step, **ex)

    def create(self):

        self._impl = Gtk.SpinButton.new_with_range(self._config["min_value"], self._config["max_value"], self._config["step"])

        self._impl._interface = self

    def _get_value(self):
        return 0

    def _set_value(self, value):
        pass
