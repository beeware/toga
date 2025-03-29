from travertino.size import at_least

from textual.validation import Number
from textual.widgets import Input as TextualInput

from .base import Widget


class TogaInput(TextualInput):
    def __init__(self, impl):
        super().__init__()
        self.interface = impl.interface
        self.impl = impl

    def on_input_changed(self, event: TextualInput.Changed) -> None:
        self.interface.on_change()

    def on_input_submitted(self, event: TextualInput.Submitted) -> None:
        self.interface.on_confirm()


class NumberInput(Widget):
    def create(self):
        self.native = TogaInput(self)
        self.native.type = "number"
        self.min = None
        self.max = None

    def get_readonly(self):
        return self.native.disabled

    def set_readonly(self, value):
        self.native.disabled = value

    def get_placeholder(self):
        return self.native.placeholder

    def set_placeholder(self, value):
        self.native.placeholder = value

    def get_value(self):
        if self.native.value == "" or self.native.value is None:
            return None
        else:
            if self.native.value != "-":
                return float(self.native.value)
            else:
                return self.native.value

    def set_value(self, value):
        try:
            if value is None:
                self.native.value = ""
            else:
                self.native.value = str(value)
        except AttributeError:
            self.native.value = ""

    def set_step(self, step):
        pass

    def set_min_value(self, value):
        self.min = value
        self.native.validators = [
            Number(minimum=self.min),
        ]

    def set_max_value(self, value):
        self.max = value
        self.native.validators = [
            Number(maximum=self.max),
        ]

    @property
    def width_adjustment(self):
        return 2

    @property
    def height_adjustment(self):
        return 2

    def rehint(self):
        self.interface.intrinsic.width = at_least(len(self.native.value) + 4)
        self.interface.intrinsic.height = 3
