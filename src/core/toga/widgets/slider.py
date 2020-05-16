from toga.handlers import wrapped_handler

from .base import Widget


class Slider(Widget):
    """ Slider widget, displays a range of values

    Args:
        id: An identifier for this widget.
        style (:obj:`Style`):
        default (float): Default value of the slider
        range (``tuple``): Min and max values of the slider in this form (min, max).
        tick_count (``int``): How many ticks in range. if None, slider is continuous.
        on_slide (``callable``): The function that is executed on_slide.
        enabled (bool): Whether user interaction is possible or not.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """
    def __init__(
            self,
            id=None,
            style=None,
            default=None,
            range=None,
            tick_count=None,
            on_slide=None,
            enabled=True,
            factory=None
    ):
        super().__init__(id=id, style=style, factory=factory)

        # Needed for _impl initialization
        self._tick_count = None
        self._on_slide = None

        self._impl = self.factory.Slider(interface=self)

        self.range = range
        self.tick_count = tick_count
        self.value = default
        self.on_slide = on_slide
        self.enabled = enabled

    MIN_WIDTH = 100

    @property
    def value(self):
        """ Current slider value.

        Returns:
            The current slider value as a ``float``.

        Raises:
            ValueError: If the new value is not in the range of min and max.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        _min, _max = self.range
        if value is None:
            final = 0.5
        elif _min <= value <= _max:
            final = value
        else:
            raise ValueError('Slider value ({}) is not in range ({}-{})'.format(value, _min, _max))
        self._impl.set_value(final)

    @property
    def range(self):
        """ Range composed of min and max slider value.

        Returns:
            Returns the range in a ``tuple`` like this (min, max)
        """
        return self._range

    @range.setter
    def range(self, range):
        default_range = (0.0, 1.0)
        _min, _max = default_range if range is None else range
        if _min > _max or _min == _max:
            raise ValueError('Range min value has to be smaller than max value.')
        self._range = (_min, _max)
        self._impl.set_range((_min, _max))

    @property
    def tick_count(self):
        return self._tick_count

    @tick_count.setter
    def tick_count(self, tick_count):
        self._tick_count = tick_count
        self._impl.set_tick_count(tick_count)

    @property
    def on_slide(self):
        """ The function for when the slider is slided

        Returns:
            The ``callable`` that is executed on slide.
        """
        return self._on_slide

    @on_slide.setter
    def on_slide(self, handler):
        self._on_slide = wrapped_handler(self, handler)
        self._impl.set_on_slide(self._on_slide)
