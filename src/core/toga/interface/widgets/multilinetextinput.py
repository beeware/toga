from .base import Widget


class MultilineTextInput(Widget):
    '''
    A multi-line text input widget
    '''
    def __init__(self, id=None, style=None, initial=None, readonly=False,
                                                            placeholder=None):
        '''
        Instantiate a new instance of the multi-line text input widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object.
                            If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param initial:     The initial value
        :type  initial:     ``str``

        :param readonly: Whether a user can write into the text input,
                        defaults to `False`
        :type  readonly: ``bool``

        :param placeholder: The placeholder text
        :type  placeholder: ``str``
        '''
        super().__init__(id=id, style=style, initial=initial,
                        readonly=readonly, placeholder=placeholder)

    def _configure(self, initial, readonly, placeholder):
        self.value = initial
        self.readonly = readonly
        self.placeholder = placeholder

    @property
    def placeholder(self):
        '''
        The placeholder text

        :rtype: ``str``
        '''
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = '' if value is None else str(value)
        self._set_placeholder(value)

    @property
    def value(self):
        '''
        The value of the multiline text input field

        :rtype: ``str``
        '''
        return self._value

    @value.setter
    def value(self, value):
        self._value = '' if value is None else str(value)
        self._set_value(self._value)
        self.rehint()

    @property
    def readonly(self):
        '''
        Whether a user can write into the text input

        :rtype: ``bool``
        '''
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._set_readonly(value)

    def clear(self):
        '''
        Clear the value
        '''
        self.value = ''

    def _set_readonly(self, value):
        raise NotImplementedError('MultilineTextInput widget must define _set_readonly()')

    def _set_placeholder(self, value):
        raise NotImplementedError('MultilineTextInput widget must define _set_placeholder()')

    def _set_value(self, value):
        raise NotImplementedError('MultilineTextInput widget must define _set_value()')
