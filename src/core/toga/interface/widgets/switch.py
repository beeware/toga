from .base import Widget


class Switch(Widget):
    """
    Switch widget, a clickable button with two stable states, True (on, checked) and False (off, unchecked)

    :param label:       Text to be shown next to the Switch
    :type label:        ``str``

    :param id:          An identifier for this widget.
    :type  id:          ``str``

    :param style:       an optional style object. If no style is provided then a
                        new one will be created for the widget.
    :type style:        :class:`colosseum.CSSNode`

    :param on_press:    Function to execute when pressed
    :type on_press:     ``callable``

    :param state        Current state of the Switch
    :type state         ``Bool`
    """

    def __init__(self, label, id=None, style=None, on_press=None, state=False):
        super().__init__(id=id, style=style, label=label, on_press=on_press, state=state)

    def _configure(self, label, on_press, state):
        self.label = label
        self.on_press = on_press
        self.state = state

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
        raise NotImplementedError('The inheriting class of {} must define _set_label()')

    @property
    def on_press(self):
        '''
        The callable function for when the switch is pressed

        :rtype: ``callable``
        '''
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = handler
        self._set_on_press(handler)

    def _set_on_press(self, value):
        pass

    @property
    def state(self):
        '''
        :returns: The state value

        :rtype: ``Bool``
        '''
        return self._get_state()

    @state.setter
    def state(self, value):
        '''
        Set the state value

        :param value: The new state value
        :type  value: ``Bool``
        '''
        if value is True:
            self._set_state(True)
        elif value is False:
            self._set_state(False)

    def _set_state(self, value):
        raise NotImplementedError('The inheriting class of {} must define _set_state()'.format(__class__))

    def _get_state(self):
        raise NotImplementedError('The inheriting class of {} must define _get_state()'.format(__class__))
