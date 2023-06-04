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
        min_date: datetime.date | None = None,
        max_date: datetime.date | None = None,
        on_change: callable | None = None,
    ):
        """Create a new DateInput widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial date to display. If not specified, the current date
            will be used.
        :param min_date: The earliest date (inclusive) that can be selected, or ``None``
            if there is no limit.
        :param max_date: The latest date (inclusive) that can be selected, or ``None``
            if there is no limit.
        :param on_change: A handler that will be invoked when the value changes.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a DateInput
        self._impl = self.factory.DateInput(interface=self)

        self.on_change = None
        self.min_date = min_date
        self.max_date = max_date

        self.value = value
        self.on_change = on_change

    @property
    def value(self) -> datetime.date:
        """The currently selected date.

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

        if self.min_date and value < self.min_date:
            value = self.min_date
        elif self.max_date and value > self.max_date:
            value = self.max_date

        self._impl.set_value(value)

    @property
    def min_date(self) -> datetime.date | None:
        """The minimum allowable date (inclusive), or ``None`` if there is no limit.

        Any existing date value will be clipped to the new minimum.

        If a new minimum date falls after the currently specified maximum date,
        a ``ValueError`` is raised.
        """
        return self._impl.get_min_date()

    @min_date.setter
    def min_date(self, value):
        if value is None:
            min_date = None
        else:
            min_date = self._convert_date(value)
            max_date = self.max_date
            if max_date and min_date > max_date:
                raise ValueError("min_date is after the current max_date")
            if self.value < min_date:
                self.value = min_date

        self._impl.set_min_date(min_date)

    @property
    def max_date(self) -> datetime.date | None:
        """The maximum allowable date (inclusive), or ``None`` if there is no limit.

        Any existing date value will be clipped to the new maximum.

        If a new maximum date falls before the currently specified minimum date,
        a ``ValueError`` is raised.
        """
        return self._impl.get_max_date()

    @max_date.setter
    def max_date(self, value):
        if value is None:
            max_date = None
        else:
            max_date = self._convert_date(value)
            min_date = self.min_date
            if min_date and max_date < min_date:
                raise ValueError("max_date is before the current min_date")
            if self.value > max_date:
                self.value = max_date

        self._impl.set_max_date(max_date)

    @property
    def on_change(self) -> callable:
        """The handler to invoke when the date value changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)


class DatePicker(DateInput):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        # 2023-05
        warnings.warn("DatePicker has been renamed DateInput.", DeprecationWarning)
        super().__init__(*args, **kwargs)
