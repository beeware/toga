import math
from decimal import InvalidOperation

from PySide6.QtWidgets import QDoubleSpinBox
from travertino.constants import CENTER
from travertino.size import at_least

from toga.widgets.numberinput import _clean_decimal

from ..libs import qt_text_align
from .base import Widget


class NumberInput(Widget):
    def create(self):
        self.native = QDoubleSpinBox()
        self.native.textChanged.connect(self.qt_on_change)

    def qt_on_change(self, value):
        self.interface.on_change()

    def get_readonly(self):
        return self.native.isReadOnly()

    def set_readonly(self, value):
        self.native.setReadOnly(value)

    def set_step(self, step):
        self.native.setSingleStep(step)
        self.native.setDecimals(abs(self.interface.step.as_tuple().exponent))

    def set_min_value(self, value):
        if value is None:
            value = -math.inf
        self.native.setMinimum(value)

    def set_max_value(self, value):
        if value is None:
            value = math.inf
        self.native.setMaximum(value)

    def get_value(self):
        try:
            value = _clean_decimal(self.native.text(), self.interface.step)
        except InvalidOperation:
            return None
        if self.interface.max is not None:
            value = min(value, self.interface.max)
        if self.interface.max is not None:
            value = max(value, self.interface.min)
        return value

    def set_value(self, value):
        if value is None:
            self.native.lineEdit().setText("")
        else:
            self.native.setValue(float(value))

    def set_text_align(self, alignment):
        self.native.setAlignment(qt_text_align(alignment, CENTER))

    def rehint(self):
        size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, size.width())
        )
        self.interface.intrinsic.height = size.height()
