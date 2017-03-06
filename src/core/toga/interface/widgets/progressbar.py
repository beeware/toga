from .base import Widget


class ProgressBar(Widget):
    '''
    Progressbar widget
    '''
    def __init__(self, id=None, style=None, max=None, value=None):
        '''
        Instantiate a new instance of the progress bar widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param max: The maximum value
        :type  max: ``int``

        :param value: The initial value
        :type  value: ``int``
        '''
        super().__init__(id=id, style=style, max=max, value=value)

    def _configure(self, max, value):
        self.value = value
        self.max = max
        self.running = False
        self.rehint()

    @property
    def value(self):
        '''
        The progress value
        
        :rtype: ``int``
        '''
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._running = self._value is not None

    @property
    def max(self):
        '''
        The maximum value

        :rtype: ``int``
        '''
        return self._max

    @max.setter
    def max(self, max):
        self._max = max
        self._set_max(max)
