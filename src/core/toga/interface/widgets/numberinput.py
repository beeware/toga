from .base import Widget


class NumberInput(Widget):
    '''
    Widget for input of a number
    '''
    def __init__(self, id=None, style=None, min_value=0, max_value=100, step=1, **ex):
        '''
        Instantiate a new instance of the Number input widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`
        
        :param min_value:   Minimum value (default 0)
        :type min_value:    ``int``

        :param max_value:   Maximum value (default 100)
        :type max_value:    ``int``

        :param step:        Step of the adjustment buttons
        :type step:         ``int``
        '''
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        super().__init__(id=id, style=style, min_value=min_value, max_value=max_value, step=step, **ex)

    def _configure(self, **kw):
        pass

    @property
    def value(self):
        '''
        Current value
        
        :rtype: ``int``
        :return: The current value
        '''
        return self._get_value()

    @value.setter
    def value(self, value):
        self._set_value(value)
