from .base import Widget


class Button(Widget):
    '''
    Button widget, a clickable button

    :param label:       Text to be shown on the button
    :type label:        ``str``

    :param id:          An identifier for this widget.
    :type  id:          ``str``

    :param style:       an optional style object. If no style is provided then a
                        new one will be created for the widget.
    :type style:        :class:`colosseum.CSSNode`

    :param on_press:    Function to execute when pressed
    :type on_press:     ``callable``
    '''
    def __init__(self, label, id=None, style=None, on_press=None):
        super().__init__(id=id, style=style, label=label, on_press=on_press)

    def _configure(self, label, on_press):
        self.label = label
        self.on_press = on_press

    @property
    def label(self):
        '''
        :returns: The label value
        :rtype: ``str``
        '''
        return self._label

    @label.setter
    def label(self, value):
        '''
        Set the label value
        
        :param value: The new label value
        :type  value: ``str``
        '''
        if value is None:
            self._label = ''
        else:
            self._label = str(value)
        self._set_label(value)
        self.rehint()

    def _set_label(self, value):
        raise NotImplementedError('Button widget must define _set_label()')

    @property
    def on_press(self):
        '''
        The callable function for when the button is pressed
        
        :rtype: ``callable``
        '''
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = handler
        self._set_on_press(handler)

    def _set_on_press(self, value):
        pass
