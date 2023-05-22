import re
from decimal import Decimal, InvalidOperation
from typing import Optional

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


def _clean_decimal_str(value):
    """Clean a string value"""
    # Replace any character that isn't a number, `.` or `-`
    value = NUMERIC_RE.sub("", value)
    # Remove any `-` not at the start of the string
    pos = 1
    while (pos := value.find("-", pos)) != -1:
        value = value[:pos] + value[pos + 1 :]

    # Only allow the first instance of `.`
    pos = value.find(".")
    if pos != -1:
        pos = pos + 1
        while (pos := value.find(".", pos)) != -1:
            value = value[:pos] + value[pos + 1 :]
            pos = value.find(".", pos)

    return value


class NumberInput(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        step: Decimal = 1,
        min_value: Optional[Decimal] = None,
        max_value: Optional[Decimal] = None,
        value: Optional[Decimal] = None,
        readonly: bool = False,
        on_change=None,
    ):
        """Create a new single-line text input widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param step: The amount that any increment/decrement operations will
            apply to the widget's current value.
        :param min_value: Optional; if provided, ``value`` will be guaranteed to
            be greater than or equal to this minimum.
        :param min_value: Optional; if provided, ``value`` will be guaranteed to
            be greater than or equal to this minimum.
        :param value: Optional; the initial value for the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param on_change: A handler that will be invoked when the the value of
            the widget changes.
        """

        super().__init__(id=id, style=style)

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
        widget's current value.
        """
        return self._step

    @step.setter
    def step(self, step):
        try:
            # See implementation notes for the reason for this conversion
            if isinstance(step, float):
                step = str(step)

            self._step = Decimal(step)
        except (ValueError, TypeError, InvalidOperation):
            raise ValueError("step must be a number")

        self._impl.set_step(self._step)

    @property
    def min_value(self) -> Optional[Decimal]:
        """The minimum bound for the widget's value.

        Returns ``None`` if there is no minimum bound.
        """
        return self._min_value

    @min_value.setter
    def min_value(self, new_min):
        try:
            # See implementation notes for the reason for this conversion
            if isinstance(new_min, float):
                new_min = str(new_min)

            new_min = Decimal(new_min)

            # Clip widget's value to the new minumum
            if self.value is not None and self.value < new_min:
                self.value = new_min
        except (TypeError, ValueError, InvalidOperation):
            if new_min is None or new_min == "":
                new_min = None
            else:
                raise ValueError("min_value must be a number or None")

        self._min_value = new_min
        self._impl.set_min_value(new_min)

    @property
    def max_value(self) -> Optional[Decimal]:
        """The maximum bound for the widget's value.

        Returns ``None`` if there is no maximum bound.
        """
        return self._max_value

    @max_value.setter
    def max_value(self, new_max):
        try:
            # See implementation notes for the reason for this conversion
            if isinstance(new_max, float):
                new_max = str(new_max)

            new_max = Decimal(new_max)

            # Clip widget's value to the new maximum
            if self.value is not None and self.value > new_max:
                self.value = new_max
        except (TypeError, ValueError, InvalidOperation):
            if new_max is None or new_max == "":
                new_max = None
            else:
                raise ValueError("max_value must be a number or None")

        self._max_value = new_max
        self._impl.set_max_value(new_max)

    @property
    def value(self) -> Optional[Decimal]:
        """Current value of the widget.

        Returns ``None`` if no value has been set on the widget.

        While the widget is being edited by the user, it is possible for the UI
        to contain text that isn't a valid value according to the min/max range.
        In this case, the widget will return a current value of ``None``.
        """
        # Get the value currently displayed by the widget. This *could*
        # be outside the min/max range.
        value = self._impl.get_value()

        # If the widget has a current value, clip it
        if value:
            if self.min_value and value < self.min_value:
                return None
            elif self.max_value and value > self.max_value:
                return None
        return value

    @value.setter
    def value(self, value):
        try:
            # Decimal(3.7) yields "3.700000000...177".
            # However, Decimal(str(3.7)) yields "3.7". If the user provides a float,
            # convert to a string first.
            if isinstance(value, float):
                value = str(value)
            value = Decimal(value)

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
    def on_change(self):
        """The handler to invoke when the value of the widget changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)
