from .base import Widget


class NumberInput(Widget):
    def __init__(self, id=None, style=None, min_value=0, max_value=100, step=1, **ex):
        super().__init__(id=id, style=style, min_value=min_value, max_value=max_value, step=step, **ex)

    def _configure(self, min, max, step):
        self.min = min
        self.max = max
        self.step = step

    @property
    def value(self):
        return self._get_value()

    @value.setter
    def value(self, value):
        self._set_value(value)
