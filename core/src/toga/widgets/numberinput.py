from __future__ import annotations

import re
import sys
import warnings
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import TYPE_CHECKING, Any, Protocol, Union

import toga
from toga.handlers import wrapped_handler

from .base import StyleT, Widget

if TYPE_CHECKING:
    if sys.version_info < (3, 10):
        from typing_extensions import TypeAlias
    else:
        from typing import TypeAlias

    NumberInputT: TypeAlias = Union[Decimal, int, float, str]

# Implementation notes
# ====================
#
# * `step`, `min` and `max` maintain an interface shadow copy of
#   their current values. This is because we use Decimal as a representation,
#   but all the implementations use floats. To ensure that we can round-trip
#   step/min/max values, we need to keep a local copy.
# * Decimal(3.7) yields "3.700000000...177". However, Decimal(str(3.7)) yields
#   "3.7". If the user provides a float, convert to a string first to ensure
#   that we don't introduce floating point error.


NUMERIC_RE = re.compile(r"[^0-9\.-]")


def _clean_decimal(value: NumberInputT, step: NumberInputT | None = None) -> Decimal:
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


def _clean_decimal_str(value: str) -> str:
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


class OnChangeHandler(Protocol):
    def __call__(self, widget: NumberInput, /, **kwargs: Any) -> object:
        """A handler to invoke when the value is changed.

        :param widget: The NumberInput that was changed.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class NumberInput(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        step: NumberInputT = 1,
        min: NumberInputT | None = None,
        max: NumberInputT | None = None,
        value: NumberInputT | None = None,
        readonly: bool = False,
        on_change: toga.widgets.numberinput.OnChangeHandler | None = None,
        min_value: None = None,  # DEPRECATED
        max_value: None = None,  # DEPRECATED
    ):
        """Create a new number input widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param step: The amount that any increment/decrement operations will apply to
            the widget's current value.
        :param min: If provided, :any:`value` will be guaranteed to be greater than or
            equal to this minimum.
        :param max: If provided, :any:`value` will be guaranteed to be less than or
            equal to this maximum.
        :param value: The initial value for the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param on_change: A handler that will be invoked when the value of the widget
            changes.
        :param min_value: **DEPRECATED**; alias of ``min``.
        :param max_value: **DEPRECATED**; alias of ``max``.
        """
        super().__init__(id=id, style=style)

        ######################################################################
        # 2023-06: Backwards compatibility
        ######################################################################
        if min_value is not None:
            if min is not None:
                raise ValueError("Cannot specify both min and min_value")
            else:
                warnings.warn(
                    "NumberInput.min_value has been renamed NumberInput.min",
                    DeprecationWarning,
                )
                min = min_value
        if max_value is not None:
            if max is not None:
                raise ValueError("Cannot specify both max and max_value")
            else:
                warnings.warn(
                    "NumberInput.max_value has been renamed NumberInput.max",
                    DeprecationWarning,
                )
                max = max_value
        ######################################################################
        # End backwards compatibility
        ######################################################################

        # The initial setting of min requires calling get_value(),
        # which in turn interrogates min. Prime those values with
        # an empty starting value
        self._min: Decimal | None = None
        self._max: Decimal | None = None

        self.on_change = None
        self._impl = self.factory.NumberInput(interface=self)

        self.readonly = readonly
        self.step = step
        self.min = min
        self.max = max
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
    def readonly(self, value: object) -> None:
        self._impl.set_readonly(value)

    @property
    def step(self) -> Decimal:
        """The amount that any increment/decrement operations will apply to the
        widget's current value. (Not all backends provide increment and
        decrement buttons.)
        """
        return self._step

    @step.setter
    def step(self, step: NumberInputT) -> None:
        try:
            self._step = _clean_decimal(step)
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError("step must be a number")

        self._impl.set_step(self._step)

        # Re-assigning the min and max value forces the min/max to be re-quantized.
        self.min = self.min
        self.max = self.max

    @property
    def min(self) -> Decimal | None:
        """The minimum bound for the widget's value.

        Returns :any:`None` if there is no minimum bound.

        When setting this property, the current :attr:`value` and :attr:`max` will be
        clipped against the new minimum value.
        """
        return self._min

    @min.setter
    def min(self, new_min: NumberInputT | None) -> None:
        try:
            new_min = _clean_decimal(new_min, self.step)

            # Clip widget's value to the new minimum
            if self.value is not None and self.value < new_min:
                self.value = new_min
        except (TypeError, ValueError, InvalidOperation):
            if new_min is None or new_min == "":
                new_min = None
            else:
                raise ValueError("min must be a number or None")

        # Clip the max value if it's inconsistent with the new min
        if self.max is not None and new_min is not None and new_min > self.max:
            self.max = new_min

        self._min = new_min
        self._impl.set_min_value(new_min)

    @property
    def max(self) -> Decimal | None:
        """The maximum bound for the widget's value.

        Returns :any:`None` if there is no maximum bound.

        When setting this property, the current :attr:`value` and :attr:`min` will be
        clipped against the new maximum value.
        """
        return self._max

    @max.setter
    def max(self, new_max: NumberInputT | None) -> None:
        try:
            new_max = _clean_decimal(new_max, self.step)

            # Clip widget's value to the new maximum
            if self.value is not None and self.value > new_max:
                self.value = new_max
        except (TypeError, ValueError, InvalidOperation):
            if new_max is None or new_max == "":
                new_max = None
            else:
                raise ValueError("max must be a number or None")

        # Clip the min value if it's inconsistent with the new max
        if self.min is not None and new_max is not None and new_max < self.min:
            self.min = new_max

        self._max = new_max
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
            if self.min is not None and value < self.min:
                return self.min
            elif self.max is not None and value > self.max:
                return self.max
        return value

    @value.setter
    def value(self, value: NumberInputT | None) -> None:
        try:
            value = _clean_decimal(value, self.step)

            if self.min is not None and value < self.min:
                value = self.min
            elif self.max is not None and value > self.max:
                value = self.max
        except (TypeError, ValueError, InvalidOperation):
            if value is None or value == "":
                value = None
            else:
                raise ValueError("value must be a number or None")

        self._impl.set_value(value)
        self.refresh()

    @property
    def on_change(self) -> OnChangeHandler:
        """The handler to invoke when the value of the widget changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler: toga.widgets.numberinput.OnChangeHandler) -> None:
        self._on_change = wrapped_handler(self, handler)

    ######################################################################
    # 2023-06: Backwards compatibility
    ######################################################################

    @property
    def min_value(self) -> Decimal | None:
        """**DEPRECATED**; alias of :attr:`min`."""
        warnings.warn(
            "NumberInput.min_value has been renamed NumberInput.min",
            DeprecationWarning,
        )
        return self.min

    @min_value.setter
    def min_value(self, value: NumberInputT | None) -> None:
        warnings.warn(
            "NumberInput.min_value has been renamed NumberInput.min",
            DeprecationWarning,
        )
        self.min = value

    @property
    def max_value(self) -> Decimal | None:
        """**DEPRECATED**; alias of :attr:`max`."""
        warnings.warn(
            "NumberInput.max_value has been renamed NumberInput.max",
            DeprecationWarning,
        )
        return self.max

    @max_value.setter
    def max_value(self, value: NumberInputT | None) -> None:
        warnings.warn(
            "NumberInput.max_value has been renamed NumberInput.max",
            DeprecationWarning,
        )
        self.max = value
