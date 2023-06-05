from __future__ import annotations

import datetime
import warnings

from toga.handlers import wrapped_handler

from .base import Widget


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

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial date to display. If not specified, the current date
            will be used.
        :param min_value: The earliest date (inclusive) that can be selected, or ``None``
            if there is no limit.
        :param max_value: The latest date (inclusive) that can be selected, or ``None``
            if there is no limit.
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
        """The currently selected date.

        If this property is set to a value outside of the min/max range, it will be
        clipped.

        A value of ``None`` will be converted into today's date.
        """
        return self._impl.get_value()

    def _convert_date(self, value):
        if value is None:
            return datetime.date.today()
        elif isinstance(value, datetime.datetime):
            return value.date()
        elif isinstance(value, datetime.date):
            return value
        elif isinstance(value, str):
            return datetime.date.fromisoformat(value)
        else:
            raise TypeError("Not a valid date value")

    @value.setter
    def value(self, value):
        value = self._convert_date(value)

        if self.min_value and value < self.min_value:
            value = self.min_value
        elif self.max_value and value > self.max_value:
            value = self.max_value

        self._impl.set_value(value)

    @property
    def min_value(self) -> datetime.date | None:
        """The minimum allowable date (inclusive), or ``None`` if there is no limit.

        Any existing date value will be clipped to the new minimum.

        If a new minimum date falls after the currently specified maximum date,
        a ``ValueError`` is raised.
        """
        return self._impl.get_min_date()

    @min_value.setter
    def min_value(self, value):
        if value is None:
            min_value = None
        else:
            min_value = self._convert_date(value)
            max_value = self.max_value
            if max_value and min_value > max_value:
                raise ValueError("min_value is after the current max_value")
            if self.value < min_value:
                self.value = min_value

        self._impl.set_min_date(min_value)

    @property
    def max_value(self) -> datetime.date | None:
        """The maximum allowable date (inclusive), or ``None`` if there is no limit.

        Any existing date value will be clipped to the new maximum.

        If a new maximum date falls before the currently specified minimum date,
        a ``ValueError`` is raised.
        """
        return self._impl.get_max_date()

    @max_value.setter
    def max_value(self, value):
        if value is None:
            max_value = None
        else:
            max_value = self._convert_date(value)
            min_value = self.min_value
            if min_value and max_value < min_value:
                raise ValueError("max_value is before the current min_value")
            if self.value > max_value:
                self.value = max_value

        self._impl.set_max_date(max_value)

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
