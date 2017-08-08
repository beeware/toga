from .base import Widget


class Range:
    def __init__(self, max, min):
        self.max = max
        self.min = min


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
    :type range:        ``Range``

    :param on_slide:    Function to execute on slide
    :type on_slide:     ``callable``

    :param enabled:     Whether user interaction is possible or not.
    :type enabled:      ``Bool``
    """

    def __init__(self, id=None, style=None, default=None, range=None, on_slide=None, enabled=True):
        super().__init__(id=id, style=style, default=default, range=range, on_slide=on_slide, enabled=enabled)

    def _configure(self, default, range, on_slide, enabled):
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
        return self._get_value()

    @value.setter
    def value(self, value):
        """
        Set the value of the slider.

        :param value:       The new slider value
        :type value:        ``int or float``
        """
        _min, _max = self.range
        if value is None:
            self._set_value(.5)
        elif _min < value < _max:
            self._set_value(value)
        else:
            raise Exception('Slider value ({}) is not in range ({}-{})'.format(value, _min, _max))

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
        self._set_range(Range(_min, _max))

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
        self._set_on_slide(handler)

    def _set_on_slide(self, value):
        pass

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
        self._set_enabled(value)
