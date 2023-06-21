from __future__ import annotations

import datetime
import warnings

from toga.handlers import wrapped_handler

from .base import Widget

# This accommodates the ranges of all existing implementations:
#  * datetime.date: 1 - 9999
#  * Android: approx 5,800,000 BC - 5,800,000
#  * Windows: 1753 - 9998
MIN_DATE = datetime.date(1800, 1, 1)
MAX_DATE = datetime.date(8999, 12, 31)


class DateInput(Widget):
    _MIN_WIDTH = 200

    def __init__(
        self,
        id=None,
        style=None,
        value: datetime.date | None = None,
        min_value: datetime.date | None = None,
        max_value: datetime.date | None = None,
        on_change: callable | None = None,
    ):
        """Create a new DateInput widget.

        Inherits from :class:`toga.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial date to display. If not specified, the current date
            will be used.
        :param min_value: The earliest date (inclusive) that can be selected.
        :param max_value: The latest date (inclusive) that can be selected.
        :param on_change: A handler that will be invoked when the value changes.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a DateInput
        self._impl = self.factory.DateInput(interface=self)

        self.on_change = None
        self.min_value = min_value
        self.max_value = max_value

        self.value = value
        self.on_change = on_change

    @property
    def value(self) -> datetime.date:
        """The currently selected date. A value of ``None`` will be converted into
        today's date.

        If this property is set to a value outside of the min/max range, it will be
        clipped.
        """
        return self._impl.get_value()

    def _convert_date(self, value, *, check_range):
        if value is None:
            value = datetime.date.today()
        elif isinstance(value, datetime.datetime):
            value = value.date()
        elif isinstance(value, datetime.date):
            pass
        elif isinstance(value, str):
            value = datetime.date.fromisoformat(value)
        else:
            raise TypeError("Not a valid date value")

        if check_range:
            if value < MIN_DATE:
                raise ValueError(f"The lowest supported date is {MIN_DATE.isoformat()}")
            if value > MAX_DATE:
                raise ValueError(
                    f"The highest supported date is {MAX_DATE.isoformat()}"
                )

        return value

    @value.setter
    def value(self, value):
        value = self._convert_date(value, check_range=False)

        if value < self.min_value:
            value = self.min_value
        elif value > self.max_value:
            value = self.max_value

        self._impl.set_value(value)

    @property
    def min_value(self) -> datetime.date:
        """The minimum allowable date (inclusive). A value of ``None`` will be converted
        into the lowest supported date of 1800-01-01.

        The existing ``value`` and ``max_value`` will be clipped to the new minimum.

        :raises ValueError: If set to a date outside of the supported range.
        """
        return self._impl.get_min_date()

    @min_value.setter
    def min_value(self, value):
        if value is None:
            min_value = MIN_DATE
        else:
            min_value = self._convert_date(value, check_range=True)

        if self.max_value < min_value:
            self._impl.set_max_date(min_value)
        self._impl.set_min_date(min_value)
        if self.value < min_value:
            self.value = min_value

    @property
    def max_value(self) -> datetime.date:
        """The maximum allowable date (inclusive). A value of ``None`` will be converted
        into the highest supported date of 8999-12-31.

        The existing ``value`` and ``min_value`` will be clipped to the new maximum.

        :raises ValueError: If set to a date outside of the supported range.
        """
        return self._impl.get_max_date()

    @max_value.setter
    def max_value(self, value):
        if value is None:
            max_value = MAX_DATE
        else:
            max_value = self._convert_date(value, check_range=True)

        if self.min_value > max_value:
            self._impl.set_min_date(max_value)
        self._impl.set_max_date(max_value)
        if self.value > max_value:
            self.value = max_value

    @property
    def on_change(self) -> callable:
        """The handler to invoke when the date value changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)


# 2023-05: Backwards compatibility
class DatePicker(DateInput):
    def __init__(self, *args, **kwargs):
        warnings.warn("DatePicker has been renamed DateInput.", DeprecationWarning)

        for old_name, new_name in [
            ("min_date", "min_value"),
            ("max_date", "max_value"),
        ]:
            try:
                value = kwargs.pop(old_name)
            except KeyError:
                pass
            else:
                kwargs[new_name] = value

        super().__init__(*args, **kwargs)

    @property
    def min_date(self):
        return self.min_value

    @min_date.setter
    def min_date(self, value):
        self.min_value = value

    @property
    def max_date(self):
        return self.max_value

    @max_date.setter
    def max_date(self, value):
        self.max_value = value
