from collections import namedtuple
from .base import Widget

Range = namedtuple('Range', ['min', 'max'])


class Slider(Widget):
    """
    Slider widget, displays a range of values

    :param id:          An identifier for this widget.
    :type  id:          ``str``

    :param style:       an optional style object. If no style is provided then a
                        new one will be created for the widget.
    :type style:        :class:`colosseum.CSSNode`

    :param default:     Default value of the slider
    :type default:      ``float``

    :param range:       Min and max values of the slider
    :type range:        ``tuple``

    :param on_slide:    Function to execute on slide
    :type on_slide:     ``callable``

    :param enabled:     Whether user interaction is possible or not.
    :type enabled:      ``Bool``
    """

    def __init__(self, id=None, style=None, default=None, range=None, on_slide=None, enabled=True, factory=None):
        super().__init__(id=id, style=style, factory=factory)
        self._impl = self.factory.Slider(interface=self)

        self.range = range
        self.value = default
        self.on_slide = on_slide
        self.enabled = enabled

    @property
    def value(self):
        """
        :returns: The current slider value
        :rtype: ``float``
        """
        self._value = self._impl.get_value()
        return self._value

    @value.setter
    def value(self, value):
        """
        Set the value of the slider.

        :param value:       The new slider value
        :type value:        ``int or float``
        """
        _min, _max = self.range
        if value is None:
            self._value = 0.5
        elif _min < value < _max:
            self._value = value
        else:
            raise Exception('Slider value ({}) is not in range ({}-{})'.format(value, _min, _max))
        self._impl.set_value(self._value)

    @property
    def range(self):
        """
        Range composed of min and max slider value.

        :rtype: ``collections.namedtuple``
        """
        return self._range

    @range.setter
    def range(self, range):
        default_range = (0.0, 1.0)
        _min, _max = default_range if range is None else range
        if _min > _max or _min == _max:
            raise Exception('Range min value has to be smaller than max value.')
        self._range = Range(_min, _max)
        self._impl.set_range(Range(_min, _max))

    @property
    def on_slide(self):
        """
        The function for when the slider is slided

        :rtype:     ``callable``
        """
        return self._on_press

    @on_slide.setter
    def on_slide(self, handler):
        """
`       Set the function that is going to be executed on slide.

        :param handler:     The function to be executed
        :type handler:      ``callable`
        """
        self._on_press = handler
        # self._set_on_slide(handler)

    @property
    def enabled(self):
        """
        Indicates whether slider interaction is possible or not.

        :rtype:     ``Bool``
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """
        Set the enabled state of the slider

        :param value:       The new enabled value
        :type value:        ``Bool``
        """
        if value is True:
            self._enabled = True
        elif value is False:
            self._enabled = False
        else:
            raise Exception('value must be of type Bool')
        self._impl.set_enabled(value)
