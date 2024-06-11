from __future__ import annotations

import datetime
import warnings
from typing import Any, Protocol

import toga
from toga.handlers import wrapped_handler

from .base import StyleT, Widget


class OnChangeHandler(Protocol):
    def __call__(self, widget: TimeInput, /, **kwargs: Any) -> object:
        """A handler to invoke when the time input is changed.

        :param widget: The TimeInput that was changed.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class TimeInput(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        value: datetime.time | None = None,
        min: datetime.time | None = None,
        max: datetime.time | None = None,
        on_change: toga.widgets.timeinput.OnChangeHandler | None = None,
    ):
        """Create a new TimeInput widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial time to display. If not specified, the current time
            will be used.
        :param min: The earliest time (inclusive) that can be selected.
        :param max: The latest time (inclusive) that can be selected.
        :param on_change: A handler that will be invoked when the value changes.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a TimeInput
        self._impl = self.factory.TimeInput(interface=self)

        self.on_change = None
        self.min = min
        self.max = max

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

    @value.setter
    def value(self, value: object) -> None:
        value = self._convert_time(value)

        if value < self.min:
            value = self.min
        elif value > self.max:
            value = self.max

        self._impl.set_value(value)

    def _convert_time(self, value: object) -> datetime.time:
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

    @property
    def min(self) -> datetime.time:
        """The minimum allowable time (inclusive). A value of ``None`` will be converted
        into 00:00:00.

        When setting this property, the current :attr:`value` and :attr:`max` will be
        clipped against the new minimum value.
        """
        return self._impl.get_min_time()

    @min.setter
    def min(self, value: object) -> None:
        if value is None:
            min = datetime.time(0, 0, 0)
        else:
            min = self._convert_time(value)

        if self.max < min:
            self._impl.set_max_time(min)
        self._impl.set_min_time(min)
        if self.value < min:
            self.value = min

    @property
    def max(self) -> datetime.time:
        """The maximum allowable time (inclusive). A value of ``None`` will be converted
        into 23:59:59.

        When setting this property, the current :attr:`value` and :attr:`min` will be
        clipped against the new maximum value.
        """
        return self._impl.get_max_time()

    @max.setter
    def max(self, value: object) -> None:
        if value is None:
            max = datetime.time(23, 59, 59)
        else:
            max = self._convert_time(value)

        if self.min > max:
            self._impl.set_min_time(max)
        self._impl.set_max_time(max)
        if self.value > max:
            self.value = max

    @property
    def on_change(self) -> OnChangeHandler:
        """The handler to invoke when the time value changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler: toga.widgets.timeinput.OnChangeHandler) -> None:
        self._on_change = wrapped_handler(self, handler)


# 2023-05: Backwards compatibility
class TimePicker(TimeInput):
    def __init__(self, *args: Any, **kwargs: Any):
        warnings.warn("TimePicker has been renamed TimeInput", DeprecationWarning)

        for old_name, new_name in [
            ("min_time", "min"),
            ("max_time", "max"),
        ]:
            try:
                value = kwargs.pop(old_name)
                warnings.warn(
                    f"TimePicker.{old_name} has been renamed TimeInput.{new_name}",
                    DeprecationWarning,
                )
            except KeyError:
                pass
            else:
                kwargs[new_name] = value

        super().__init__(*args, **kwargs)

    @property
    def min_time(self) -> datetime.time:
        warnings.warn(
            "TimePicker.min_time has been renamed TimeInput.min", DeprecationWarning
        )
        return self.min

    @min_time.setter
    def min_time(self, value: object) -> None:
        warnings.warn(
            "TimePicker.min_time has been renamed TimeInput.min", DeprecationWarning
        )
        self.min = value

    @property
    def max_time(self) -> datetime.time:
        warnings.warn(
            "TimePicker.max_time has been renamed TimeInput.max", DeprecationWarning
        )
        return self.max

    @max_time.setter
    def max_time(self, value: object) -> None:
        warnings.warn(
            "TimePicker.max_time has been renamed TimeInput.max", DeprecationWarning
        )
        self.max = value
