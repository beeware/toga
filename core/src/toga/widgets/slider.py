from contextlib import contextmanager
from typing import Optional, Tuple

from toga.handlers import wrapped_handler

from .base import Widget


class Slider(Widget):
    def __init__(
        self,
        id=None,
        style=None,
        value=None,
        range=(0, 1),
        tick_count=None,
        on_change=None,
        on_press=None,
        on_release=None,
        enabled=True,
    ):
        """Create a new slider widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: Initial :any:`value`: defaults to the mid-point of the range.
        :param range: Initial :any:`range`: defaults to (0, 1).
        :param tick_count: Initial :any:`tick_count`.
        :param on_change: Initial :any:`on_change` handler.
        :param on_press: Initial :any:`on_press` handler.
        :param on_release: Initial :any:`on_release` handler.
        :param enabled: Whether the user can interact with the widget.
        """
        super().__init__(id=id, style=style)

        # Needed for _impl initialization
        self._tick_count = None
        self._on_change = None

        self._impl = self.factory.Slider(interface=self)
        self._sync_suppressed = False
        self._value = None
        self.range = range
        self.tick_count = tick_count

        # IMPORTANT NOTE: Setting value before on_change in order to not
        # call it in constructor. Please do not move it from here.
        self.value = value

        self.on_change = on_change
        self.enabled = enabled
        self.on_press = on_press
        self.on_release = on_release

    _MIN_WIDTH = 100

    # Normally we would use the native widget as the single source of truth for any
    # user-modifiable state. However, some of the native widgets are based on ints or
    # 32-bit floats, and aren't able to store a 64-bit Python float without loss of
    # accuracy. So we store the value in the interface instead, and require the
    # implementation to call _sync_value whenever it's changed by the user.
    @property
    def value(self) -> float:
        """Current value.

        :raises ValueError: If set to a value which is outside of the :any:`range`.
        """
        return self._value

    @value.setter
    def value(self, value):
        if value is None:
            final = (self.min + self.max) / 2
        elif self.min <= value <= self.max:
            final = value
        else:
            raise ValueError(
                "Slider value ({}) is not in range ({}-{})".format(
                    value, self.min, self.max
                )
            )
        self._value = final
        with self._suppress_sync():
            self._impl.set_value(final)
        if self.on_change:
            self.on_change(self)

    @contextmanager
    def _suppress_sync(self):
        self._sync_suppressed = True
        yield
        self._sync_suppressed = False

    def _sync_value(self):
        if not self._sync_suppressed:
            self._value = self._impl.get_value()
            if self.on_change:
                self.on_change(self)

    @property
    def range(self) -> Tuple[float]:
        """Range of allowed values, in the form (min, max).

        :raises ValueError: If the min is not strictly less than the max.
        """
        return self.min, self.max

    @range.setter
    def range(self, range):
        _min, _max = range
        if _min > _max or _min == _max:
            raise ValueError("Range min value has to be smaller than max value.")
        self._min = _min
        self._max = _max

        with self._suppress_sync():
            self._impl.set_range((_min, _max))
            old_value = self._value
            if old_value is not None:
                # Clip the value within the new range.
                self._value = max(_min, min(_max, old_value))

                # Even if the value wasn't clipped, this may be necessary to update the
                # slider position in backends that don't implement set_range.
                self._impl.set_value(self._value)

        if self.on_change and (old_value != self._value):
            self.on_change(self)

    @property
    def min(self) -> float:
        """Minimum allowed value.

        This property is read-only, and depends on the value of :any:`range`.
        """
        return self._min

    @property
    def max(self) -> float:
        """Maximum allowed value.

        This property is read-only, and depends on the value of :any:`range`.
        """
        return self._max

    @property
    def tick_count(self) -> Optional[int]:
        """Number of tick marks to display on the slider.

        * If this is ``None``, the slider will be continuous.
        * Otherwise, the slider will be discrete, and will have the given number of
          possible values, equally spaced within the :any:`range`.

        :raises ValueError: If set to a count which is not at least 2 (for the min and
            max).
        """
        return self._tick_count

    @tick_count.setter
    def tick_count(self, tick_count):
        if (tick_count is not None) and (tick_count < 2):
            raise ValueError("Tick count must be at least 2")
        self._tick_count = tick_count
        self._impl.set_tick_count(tick_count)

    @property
    def tick_step(self) -> float:
        """Difference in value between two adjacent ticks, or ``None`` if the
        slider is continuous.

        This property is read-only, and depends on the values of :any:`tick_count` and
        :any:`range`.
        """
        if self.tick_count is None:
            return None
        return (self.max - self.min) / (self.tick_count - 1)

    @property
    def tick_value(self) -> Optional[int]:
        """Value of the slider, measured in ticks.

        * If the slider is continuous, this property returns ``None``.
        * Otherwise, it returns an integer between 1 (representing :any:`min`) and
          :any:`tick_count` (representing :any:`max`).

        :raises ValueError: If set to anything inconsistent with the rules above.
        """
        if self.tick_count is not None and self.value is not None:
            return round((self.value - self.min) / self.tick_step) + 1
        else:
            return None

    @tick_value.setter
    def tick_value(self, tick_value):
        if tick_value is not None and self.tick_count is None:
            raise ValueError("Cannot set tick value when tick count is None")
        if tick_value is not None:
            self.value = self.min + (tick_value - 1) * self.tick_step

    @property
    def on_change(self) -> callable:
        """Handler to invoke when the value of the slider is changed, either by the user
        or programmatically.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)

    @property
    def on_press(self) -> callable:
        """Handler to invoke when when the user presses the slider before changing it."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)

    @property
    def on_release(self) -> callable:
        """Handler to invoke when the user releases the slider after changing it."""
        return self._on_release

    @on_release.setter
    def on_release(self, handler):
        self._on_release = wrapped_handler(self, handler)
        self._impl.set_on_release(self._on_release)
