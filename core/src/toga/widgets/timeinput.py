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
        min_time: datetime.time | None = None,
        max_time: datetime.time | None = None,
        on_change=None,
    ):
        """Create a new TimeInput widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial time to display. Optional; if not specified,
            today's time will be used.
        :param min_time: Optional; if provided, the earliest time (inclusive)
            that can be selected.
        :param max_time: Optional; if provided, the latest time (inclusive)
            that can be selected.
        :param on_change: A handler that will be invoked when the switch changes
            value.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a TimeInput
        self._impl = self.factory.TimeInput(interface=self)

        self.on_change = None
        self.min_time = min_time
        self.max_time = max_time

        self.value = value
        self.on_change = on_change

    @property
    def value(self) -> datetime.time:
        """The currently selected time.

        A value of ``None`` will be converted into the current time, rounding
        to the nearest minute.

        If a ``datetime`` object is provided, the time portion will be extracted.

        If a string is provided, it will be parsed as an ISO8601 format time
        string. (i.e., "06:12")
        """
        return self._impl.get_value()

    def _convert_time(self, value):
        if value is None:
            return datetime.datetime.now().time().replace(second=0, microsecond=0)
        elif isinstance(value, datetime.datetime):
            return value.time()
        elif isinstance(value, datetime.time):
            return value
        elif isinstance(value, str):
            return datetime.time.fromisoformat(value)
        else:
            raise TypeError("Not a valid time value")

    @value.setter
    def value(self, value):
        value = self._convert_time(value)

        if self.min_time and value < self.min_time:
            value = self.min_time
        elif self.max_time and value > self.max_time:
            value = self.max_time

        self._impl.set_value(value)

    @property
    def min_time(self) -> datetime.time | None:
        """The minimum allowable time (inclusive) for the widget.

        If provided, times earlier than the provided time will not be available
        for selection. Any existing time value will be clipped to the new
        minimum.

        The value provided for the minimum time will be interpreted using the
        same rules as ``value``, with a value of ``None`` removing any minimum
        bound on time selection.

        If a new minimum time falls after the currently specified maximum time,
        a ``ValueError`` is raised.
        """
        return self._impl.get_min_time()

    @min_time.setter
    def min_time(self, value):
        if value is None:
            min_time = None
        else:
            min_time = self._convert_time(value)
            max_time = self.max_time
            if max_time and min_time > max_time:
                raise ValueError("min_time is after the current max_time")
            if self.value < min_time:
                self.value = min_time

        self._impl.set_min_time(min_time)

    @property
    def max_time(self) -> datetime.time | None:
        """The maximum allowable time (inclusive) for the widget.

        If provided, times after than the provided time will not be available
        for selection. Any existing time value will be clipped to the new
        maximum.

        The value provided for the maximum time will be interpreted using the
        same rules as ``value``, with a value of ``None`` removing any maximum
        bound on time selection.

        If a new maximum time falls after the currently specified minimum time,
        a ``ValueError`` is raised.
        """
        return self._impl.get_max_time()

    @max_time.setter
    def max_time(self, value):
        if value is None:
            max_time = None
        else:
            max_time = self._convert_time(value)
            min_time = self.min_time
            if min_time and max_time < min_time:
                raise ValueError("max_time is before the current min_time")
            if self.value > max_time:
                self.value = max_time

        self._impl.set_max_time(max_time)

    @property
    def on_change(self):
        """The handler to invoke when the time value changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)


class TimePicker(TimeInput):  # pragma: no cover
    def __init__(self, *args, **kwargs):
        # 2023-05
        warnings.warn("TimePicker has been renamed TimeInput.", DeprecationWarning)
        super().__init__(*args, **kwargs)
