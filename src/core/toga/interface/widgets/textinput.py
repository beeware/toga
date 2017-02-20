from .base import Widget


class TextInput(Widget):
    '''
    Text input widget
    '''
    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False):
        '''
        Instantiate a new instance of the text input widget

        :param id:          An identifier for this widget.
        :type  id:          ``str``

        :param style:       an optional style object. If no style is provided then a
                            new one will be created for the widget.
        :type style:        :class:`colosseum.CSSNode`

        :param initial: The initial text
        :type  initial: ``str``
        
        :param placeholder: The placeholder text
        :type  placeholder: ``str``
        
        :param readonly: Whether a user can write into the text input, defaults to `False`
        :type  readonly: ``bool``
        '''
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)

    def _configure(self, initial, placeholder, readonly):
        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial
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

    @property
    def placeholder(self):
        '''
        The placeholder text
        
        :rtype: ``str``
        '''
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        if value is None:
            self._placeholder = ''
        else:
            self._placeholder = str(value)
        self._set_placeholder(value)

    @property
    def value(self):
        '''
        The value of the text input field
        
        :rtype: ``str``
        '''
        return self._get_value()

    @value.setter
    def value(self, value):
        if value is None:
            v = ''
        else:
            v = str(value)
        self._set_value(v)
        self.rehint()

    def clear(self):
        '''
        Clear the value
        '''
        self.value = ''

    def _set_readonly(self, value):
        raise NotImplementedError('TextInput widget must define _set_readonly()')

    def _set_placeholder(self, value):
        raise NotImplementedError('TextInput widget must define _set_placeholder()')

    def _set_value(self, value):
        raise NotImplementedError('TextInput widget must define _set_value()')
