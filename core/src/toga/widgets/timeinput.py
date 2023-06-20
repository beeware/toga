from __future__ import annotations

import datetime
import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class TimeInput(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        value: datetime.time | None = None,
        min_value: datetime.time | None = None,
        max_value: datetime.time | None = None,
        on_change: callable | None = None,
    ):
        """Create a new TimeInput widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial time to display. If not specified, the current time
            will be used.
        :param min_value: The earliest time (inclusive) that can be selected.
        :param max_value: The latest time (inclusive) that can be selected.
        :param on_change: A handler that will be invoked when the value changes.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a TimeInput
        self._impl = self.factory.TimeInput(interface=self)

        self.on_change = None
        self.min_value = min_value
        self.max_value = max_value

        self.value = value
        self.on_change = on_change

    @property
    def value(self) -> datetime.time:
        """The currently selected time. A value of ``None`` will be converted into the
        current time.

        If this property is set to a value outside of the min/max range, it will be
        clipped.
        """
        return self._impl.get_value()

    def _convert_time(self, value):
        if value is None:
            value = datetime.datetime.now().time()
        elif isinstance(value, datetime.datetime):
            value = value.time()
        elif isinstance(value, datetime.time):
            pass
        elif isinstance(value, str):
            value = datetime.time.fromisoformat(value)
        else:
            raise TypeError("Not a valid time value")

        return value.replace(microsecond=0)

    @value.setter
    def value(self, value):
        value = self._convert_time(value)

        if value < self.min_value:
            value = self.min_value
        elif value > self.max_value:
            value = self.max_value

        self._impl.set_value(value)

    @property
    def min_value(self) -> datetime.time:
        """The minimum allowable time (inclusive). A value of ``None`` will be converted
        into 00:00:00.

        The existing ``value`` and ``max_value`` will be clipped to the new minimum.
        """
        return self._impl.get_min_time()

    @min_value.setter
    def min_value(self, value):
        if value is None:
            min_value = datetime.time(0, 0, 0)
        else:
            min_value = self._convert_time(value)

        if self.max_value < min_value:
            self._impl.set_max_time(min_value)
        self._impl.set_min_time(min_value)
        if self.value < min_value:
            self.value = min_value

    @property
    def max_value(self) -> datetime.time:
        """The maximum allowable time (inclusive). A value of ``None`` will be converted
        into 23:59:59.

        The existing ``value`` and ``min_value`` will be clipped to the new maximum.
        """
        return self._impl.get_max_time()

    @max_value.setter
    def max_value(self, value):
        if value is None:
            max_value = datetime.time(23, 59, 59)
        else:
            max_value = self._convert_time(value)

        if self.min_value > max_value:
            self._impl.set_min_time(max_value)
        self._impl.set_max_time(max_value)
        if self.value > max_value:
            self.value = max_value

    @property
    def on_change(self) -> callable:
        """The handler to invoke when the time value changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)


# 2023-05: Backwards compatibility
class TimePicker(TimeInput):
    def __init__(self, *args, **kwargs):
        warnings.warn("TimePicker has been renamed TimeInput", DeprecationWarning)

        for old_name, new_name in [
            ("min_time", "min_value"),
            ("max_time", "max_value"),
        ]:
            try:
                value = kwargs.pop(old_name)
            except KeyError:
                pass
            else:
                kwargs[new_name] = value

        super().__init__(*args, **kwargs)

    @property
    def min_time(self):
        return self.min_value

    @min_time.setter
    def min_time(self, value):
        self.min_value = value

    @property
    def max_time(self):
        return self.max_value

    @max_time.setter
    def max_time(self, value):
        self.max_value = value
