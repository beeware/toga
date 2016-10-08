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

    def rehint(self):
        # print("REHINT", self, self._impl.get_preferred_width(), self._impl.get_preferred_height(), getattr(self, '_fixed_height', False), getattr(self, '_fixed_width', False))
        hints = {}
        width = self._impl.get_preferred_width()
        minimum_width = width[0]
        natural_width = width[1]

        height = self._impl.get_preferred_height()
        minimum_height = height[0]
        natural_height = height[1]

        if minimum_width > 0:
            hints['min_width'] = minimum_width
        if minimum_height > 0:
            hints['min_height'] = minimum_height
        if natural_height > 0:
            hints['height'] = natural_height

        if hints:
            self.style.hint(**hints)
