from .base import Widget


class NumberInput(Widget):
    '''
    Widget for input of a number
    '''

    def __init__(self, id=None, style=None, factory=None,
                 min_value=0, max_value=100, step=1, **ex):
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
        super().__init__(id=id, style=style, factory=factory)
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._impl = self.factory.NumberInput(interface=self)

    @property
    def value(self):
        '''
        Current value
        
        :rtype: ``int``
        :return: The current value
        '''
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        self._impl.set_value(value)
