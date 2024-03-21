from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from contextlib import contextmanager

from toga.handlers import wrapped_handler

from .base import Widget


class Slider(Widget):
    def __init__(
        self,
        id: str | None = None,
        style=None,
        value: float | None = None,
        min: float = None,  # Default to 0.0 when range is removed
        max: float = None,  # Default to 1.0 when range is removed
        tick_count: int | None = None,
        on_change: callable | None = None,
        on_press: callable | None = None,
        on_release: callable | None = None,
        enabled: bool = True,
        range: tuple[float, float] | None = None,  # DEPRECATED
    ):
        """Create a new Slider widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param value: Initial :any:`value` of the slider. Defaults to the mid-point of
            the range.
        :param min: Initial minimum value of the slider. Defaults to 0.
        :param max: Initial maximum value of the slider. Defaults to 1.
        :param tick_count: Initial :any:`tick_count` for the slider. If :any:`None`, the
            slider will be continuous.
        :param on_change: Initial :any:`on_change` handler.
        :param on_press: Initial :any:`on_press` handler.
        :param on_release: Initial :any:`on_release` handler.
        :param enabled: Whether the user can interact with the widget.
        :param range: **DEPRECATED**; use ``min`` and ``max`` instead. Initial
            :any:`range` of the slider. Defaults to ``(0, 1)``.
        """
        super().__init__(id=id, style=style)
        self._impl = self.factory.Slider(interface=self)

        ######################################################################
        # 2023-06: Backwards compatibility
        ######################################################################
        if range is not None:
            if min is not None or max is not None:
                raise ValueError(
                    "range cannot be specified if min and max are specified"
                )
            else:
                warnings.warn(
                    "Slider.range has been deprecated in favor of Slider.min and Slider.max",
                    DeprecationWarning,
                )
                min, max = range
        else:
            # This provides defaults values for min/max.
            if min is None:
                min = 0.0
            if max is None:
                max = 1.0
        ######################################################################
        # End backwards compatibility
        ######################################################################

        # Set a dummy handler before installing the actual on_change, because we do not want
        # on_change triggered by the initial value being set
        self.on_change = None
        self.min = min
        self.max = max
        self.tick_count = tick_count
        if value is None:
            value = (min + max) / 2
        self.value = value

        self.on_change = on_change
        self.on_press = on_press
        self.on_release = on_release

        self.enabled = enabled

    _MIN_WIDTH = 100

    # Backends are inconsistent about when they produce events for programmatic changes,
    # so we deal with those in the interface layer.
    @contextmanager
    def _programmatic_change(self):
        old_value = self.value
        on_change = self._on_change
        self.on_change = None
        yield old_value

        self._on_change = on_change
        if self.value != old_value:
            on_change()

    @property
    def value(self) -> float:
        """Current value.

        If the slider is discrete, setting the value will round it to the nearest tick.

        :raises ValueError: If set to a value which is outside of the :any:`range`.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if value < self.min:
            value = self.min
        elif value > self.max:
            value = self.max
        with self._programmatic_change():
            self._set_value(value)

    def _set_value(self, value):
        self._impl.set_value(self._round_value(float(value)))

    def _round_value(self, value):
        step = self.tick_step
        if step is not None:
            # Round to the nearest tick.
            value = self.min + round((value - self.min) / step) * step
        return value

    @property
    def min(self) -> float:
        """Minimum allowed value.

        When setting this property, the current :attr:`value` and :attr:`max` will be
        clipped against the new minimum value.
        """
        return self._impl.get_min()

    @min.setter
    def min(self, value):
        with self._programmatic_change() as old_value:
            # Some backends will clip the current value within the range automatically,
            # but do it ourselves to be certain. In discrete mode, setting self.value also
            # rounds to the new positions of the ticks.
            _min = float(value)
            _max = self.max
            if _max < _min:
                _max = _min
                self._impl.set_max(_max)

            self._impl.set_min(_min)
            self._set_value(max(_min, min(_max, old_value)))

    @property
    def max(self) -> float:
        """Maximum allowed value.

        When setting this property, the current :attr:`value` and :attr:`min` will be
        clipped against the new maximum value.
        """
        return self._impl.get_max()

    @max.setter
    def max(self, value):
        with self._programmatic_change() as old_value:
            # Some backends will clip the current value within the range automatically,
            # but do it ourselves to be certain. In discrete mode, setting self.value also
            # rounds to the new positions of the ticks.
            _min = self.min
            _max = float(value)
            if _min > _max:
                _min = _max
                self._impl.set_min(_min)

            self._impl.set_max(_max)
            self._set_value(max(_min, min(_max, old_value)))

    @property
    def tick_count(self) -> int | None:
        """Number of tick marks to display on the slider.

        * If this is ``None``, the slider will be continuous.
        * If this is an ``int``, the slider will be discrete, and will have the given
          number of possible values, equally spaced within the :any:`range`.

        Setting this property to an ``int`` will round the current value to the nearest
        tick.

        :raises ValueError: If set to a count which is not at least 2 (for the min and
            max).

        .. note::

            On iOS, tick marks are not currently displayed, but discrete mode will
            otherwise work correctly.
        """
        return self._impl.get_tick_count()

    @tick_count.setter
    def tick_count(self, tick_count):
        if (tick_count is not None) and (tick_count < 2):
            raise ValueError("tick count must be at least 2")
        with self._programmatic_change() as old_value:
            # Some backends will round the current value to the nearest tick
            # automatically, but do it ourselves to be certain. Some backends also require
            # the value to be refreshed when moving between discrete and continuous mode,
            # because this causes a change in the native range.
            self._impl.set_tick_count(tick_count)
            self.value = old_value

    @property
    def tick_step(self) -> float | None:
        """Step between adjacent ticks.

        * If the slider is continuous, this property returns ``None``
        * If the slider is discrete, it returns the difference in value between adjacent
          ticks.

        This property is read-only, and depends on the values of :any:`tick_count` and
        :any:`range`.
        """
        if self.tick_count is None or self.max == self.min:
            return None
        return (self.max - self.min) / (self.tick_count - 1)

    @property
    def tick_value(self) -> int | None:
        """Value of the slider, measured in ticks.

        * If the slider is continuous, this property returns ``None``.
        * If the slider is discrete, it returns an integer between 1 (representing
          :any:`min`) and :any:`tick_count` (representing :any:`max`).

        :raises ValueError: If set to anything inconsistent with the rules above.
        """
        if self.tick_count is not None:
            return round((self.value - self.min) / self.tick_step) + 1
        else:
            return None

    @tick_value.setter
    def tick_value(self, tick_value):
        if self.tick_count is None:
            if tick_value is not None:
                raise ValueError("cannot set tick value when tick count is None")
        else:
            if tick_value is None:
                raise ValueError(
                    "cannot set tick value to None when tick count is not None"
                )
            self.value = self.min + (tick_value - 1) * self.tick_step

    @property
    def on_change(self) -> callable:
        """Handler to invoke when the value of the slider is changed, either by the user
        or programmatically.

        Setting the widget to its existing value will not call the handler.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)

    @property
    def on_press(self) -> callable:
        """Handler to invoke when the user presses the slider before changing it."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = wrapped_handler(self, handler)

    @property
    def on_release(self) -> callable:
        """Handler to invoke when the user releases the slider after changing it."""
        return self._on_release

    @on_release.setter
    def on_release(self, handler):
        self._on_release = wrapped_handler(self, handler)

    ######################################################################
    # 2023-06: Backwards compatibility
    ######################################################################
    @property
    def range(self) -> tuple[float, float]:
        """**DEPRECATED**; use :any:`min` and :any:`max` instead.

        Range of allowed values, in the form (min, max).

        If the provided min is greater than the max, both values will assume the value
        of the max.

        If the current value is less than the provided ``min``, the current value will
        be clipped to the minimum value. If the current value is greater than the
        provided ``max``, the current value will be clipped to the maximum value.
        """
        warnings.warn(
            "Slider.range has been deprecated in favor of Slider.min and Slider.max",
            DeprecationWarning,
        )
        return (self.min, self.max)

    @range.setter
    def range(self, range):
        warnings.warn(
            "Slider.range has been deprecated in favor of Slider.min and Slider.max",
            DeprecationWarning,
        )
        _min, _max = range
        self.min = _min
        self.max = _max


class SliderImpl(ABC):
    @abstractmethod
    def get_value(self): ...

    @abstractmethod
    def set_value(self, value): ...

    @abstractmethod
    def get_min(self): ...

    @abstractmethod
    def set_min(self, value): ...

    @abstractmethod
    def get_max(self): ...

    @abstractmethod
    def set_max(self, value): ...

    @abstractmethod
    def get_tick_count(self): ...

    @abstractmethod
    def set_tick_count(self, tick_count): ...


class IntSliderImpl(SliderImpl):
    """Base class for implementations which use integer values."""

    # Number of steps to use to approximate a continuous slider.
    CONTINUOUS_MAX = 10000

    def __init__(self):
        super().__init__()

        # Dummy values used during initialization.
        self.value = 0
        self.min = 0
        self.max = 1
        self.discrete = False

    def get_value(self):
        return self.value

    def set_value(self, value):
        span = self.max - self.min
        self.set_int_value(
            0 if span == 0 else round((value - self.min) / span * self.get_int_max())
        )
        self.value = value  # Cache the original value so we can round-trip it.

    def get_min(self):
        return self.min

    def set_min(self, value):
        self.min = value

    def get_max(self):
        return self.max

    def set_max(self, value):
        self.max = value

    def get_tick_count(self):
        return (self.get_int_max() + 1) if self.discrete else None

    def set_tick_count(self, tick_count):
        if tick_count is None:
            self.discrete = False
            self.set_int_max(self.CONTINUOUS_MAX)
        else:
            self.discrete = True
            self.set_int_max(tick_count - 1)
        self.set_ticks_visible(self.discrete)

    # Instead of calling the event handler directly, implementations should call this
    # method.
    def on_change(self):
        span = self.max - self.min
        self.value = self.min + (self.get_int_value() / self.get_int_max() * span)
        self.interface.on_change()

    @abstractmethod
    def get_int_value(self): ...

    @abstractmethod
    def set_int_value(self, value): ...

    @abstractmethod
    def get_int_max(self): ...

    @abstractmethod
    def set_int_max(self, max): ...

    @abstractmethod
    def set_ticks_visible(self, visible): ...
