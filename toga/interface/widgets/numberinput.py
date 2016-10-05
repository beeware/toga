from .base import Widget


class NumberInput(Widget):
    def __init__(self, id=None, style=None, min=0, max=100, step=1):
        super().__init__(id=id, style=style, min=min, max=max, step=step)


    def _configure(self, min, max, step):
        self.min = min
        self.max = max
        self.step = step


    @property
    def value(self):
        self._get_value()

    @value.setter
    def value(self, value):
        self._set_value(value)
