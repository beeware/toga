from __future__ import annotations

import re
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

from toga.handlers import wrapped_handler

from .base import Widget

# Implementation notes
# ====================
#
# * `step`, `min_value` and `max_value` maintain an interface shadow copy of
#   their current values. This is because we use Decimal as a representation,
#   but all the implementations use floats. To ensure that we can round-trip
#   step/min/max values, we need to keep a local copy.
# * Decimal(3.7) yields "3.700000000...177". However, Decimal(str(3.7)) yields
#   "3.7". If the user provides a float, convert to a string first to ensure
#   that we don't introduce floating point error.


NUMERIC_RE = re.compile(r"[^0-9\.-]")


def _clean_decimal(value, step=None):
    # Decimal(3.7) yields "3.700000000...177".
    # However, Decimal(str(3.7)) yields "3.7". If the user provides a float,
    # convert to a string first.
    if isinstance(value, float):
        value = str(value)
    value = Decimal(value)

    if step is not None:
        # ROUND_DOWN would not be unreasonable for manually-entered strings, but it
        # interacts badly with native increment operations that use floats. For example,
        # 1.2 might be incremented to 1.299999997, and then rounded back down to 1.2,
        # so nothing would change.
        value = value.quantize(step, rounding=ROUND_HALF_UP)
    return value


def _clean_decimal_str(value):
    """Clean a string value"""
    # Replace any character that isn't a number, `.` or `-`
    value = NUMERIC_RE.sub("", value)
    # Remove any `-` not at the start of the string
    pos = value.find("-", 1)
    while pos != -1:
        value = value[:pos] + value[pos + 1 :]
        pos = value.find("-", pos + 1)

    # Only allow the first instance of `.`
    pos = value.find(".")
    if pos != -1:
        pos = value.find(".", pos + 1)
        while pos != -1:
            value = value[:pos] + value[pos + 1 :]
            pos = value.find(".", pos + 1)

    return value


class NumberInput(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        step: Decimal = 1,
        min_value: Decimal | None = None,
        max_value: Decimal | None = None,
        value: Decimal | None = None,
        readonly: bool = False,
        on_change: callable | None = None,
    ):
        """Create a new number input widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param step: The amount that any increment/decrement operations will
            apply to the widget's current value.
        :param min_value: If provided, ``value`` will be guaranteed to
            be greater than or equal to this minimum.
        :param max_value: If provided, ``value`` will be guaranteed to
            be less than or equal to this maximum.
        :param value: The initial value for the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param on_change: A handler that will be invoked when the the value of
            the widget changes.
        """

        super().__init__(id=id, style=style)

        # The initial setting of min/min_value requires calling get_value(),
        # which in turn interrogates min/max_value. Prime those values with
        # an empty starting value
        self._min_value = None
        self._max_value = None

        self.on_change = None
        self._impl = self.factory.NumberInput(interface=self)

        self.readonly = readonly
        self.step = step
        self.min_value = min_value
        self.max_value = max_value
        self.value = value

        self.on_change = on_change

    @property
    def readonly(self) -> bool:
        """Can the value of the widget be modified by the user?

        This only controls manual changes by the user (i.e., typing at the
        keyboard). Programmatic changes are permitted while the widget has
        ``readonly`` enabled.
        """
        return self._impl.get_readonly()

    @readonly.setter
    def readonly(self, value):
        self._impl.set_readonly(value)

    @property
    def step(self) -> Decimal:
        """The amount that any increment/decrement operations will apply to the
        widget's current value. (Not all backends provide increment and
        decrement buttons.)
        """
        return self._step

    @step.setter
    def step(self, step):
        try:
            self._step = _clean_decimal(step)
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError("step must be a number")

        self._impl.set_step(self._step)

        # Re-assigning the min and max value forces the min/max to be requantized.
        self.min_value = self.min_value
        self.max_value = self.max_value

    @property
    def min_value(self) -> Decimal | None:
        """The minimum bound for the widget's value.

        Returns ``None`` if there is no minimum bound.

        If the current ``value`` is less than a newly specified ``min_value``,
        ``value`` will be clipped to conform to the new minimum.
        """
        return self._min_value

    @min_value.setter
    def min_value(self, new_min):
        try:
            new_min = _clean_decimal(new_min, self.step)

            # Clip widget's value to the new minumum
            if self.value is not None and self.value < new_min:
                self.value = new_min
        except (TypeError, ValueError, InvalidOperation):
            if new_min is None or new_min == "":
                new_min = None
            else:
                raise ValueError("min_value must be a number or None")

        if (
            self.max_value is not None
            and new_min is not None
            and new_min > self.max_value
        ):
            raise ValueError(
                f"min value of {new_min} is greater than the current max_value of {self.max_value}"
            )

        self._min_value = new_min
        self._impl.set_min_value(new_min)

    @property
    def max_value(self) -> Decimal | None:
        """The maximum bound for the widget's value.

        Returns ``None`` if there is no maximum bound.

        If the current ``value`` exceeds a newly specified ``max_value``,
        ``value`` will be clipped to conform to the new maximum.
        """
        return self._max_value

    @max_value.setter
    def max_value(self, new_max):
        try:
            new_max = _clean_decimal(new_max, self.step)

            # Clip widget's value to the new maximum
            if self.value is not None and self.value > new_max:
                self.value = new_max
        except (TypeError, ValueError, InvalidOperation):
            if new_max is None or new_max == "":
                new_max = None
            else:
                raise ValueError("max_value must be a number or None")

        if (
            self.min_value is not None
            and new_max is not None
            and new_max < self.min_value
        ):
            raise ValueError(
                f"max value of {new_max} is less than the current min_value of {self.min_value}"
            )

        self._max_value = new_max
        self._impl.set_max_value(new_max)

    @property
    def value(self) -> Decimal | None:
        """Current value of the widget, rounded to the same number of decimal
        places as :any:`step`, or ``None`` if no value has been set.

        If this property is set to a value outside of the min/max range, it will be
        clipped.

        While the widget is being edited by the user, it is possible for the UI
        to contain a value which is outside of the min/max range, or has too many
        decimal places. In this case, this property will return a value that has been
        clipped and rounded, and the visible text will be updated to match as soon as
        the widget loses focus.
        """
        # Get the value currently displayed by the widget. This *could*
        # be outside the min/max range.
        value = self._impl.get_value()

        # If the widget has a current value, clip it
        if value is not None:
            if self.min_value is not None and value < self.min_value:
                return self.min_value
            elif self.max_value is not None and value > self.max_value:
                return self.max_value
        return value

    @value.setter
    def value(self, value):
        try:
            value = _clean_decimal(value, self.step)

            if self.min_value is not None and value < self.min_value:
                value = self.min_value
            elif self.max_value is not None and value > self.max_value:
                value = self.max_value
        except (TypeError, ValueError, InvalidOperation):
            if value is None or value == "":
                value = None
            else:
                raise ValueError("value must be a number or None")

        self._impl.set_value(value)
        self.refresh()

    @property
    def on_change(self) -> callable:
        """The handler to invoke when the value of the widget changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)
