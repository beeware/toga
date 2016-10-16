from .base import Widget


class TextInput(Widget):
    """
    Widget for input of a text

    :param id:              Identifier for this widget
    :param style:           Style of the button
    :type style:            colosseum.CSS
    :param initial:         Initial text
    :type initial:          str
    :param placeholder:     Placeholder text
    :type placeholder:      str
    :param readonly:        Whether a user can write into the text input
    :type readonly:         bool
    """
    def __init__(self, id=None, style=None, initial=None, placeholder=None, readonly=False):
        super().__init__(id=id, style=style, initial=initial, placeholder=placeholder, readonly=readonly)

    def _configure(self, initial, placeholder, readonly):
        self.readonly = readonly
        self.placeholder = placeholder
        self.value = initial
        self.rehint()

    @property
    def readonly(self):
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._set_readonly(value)

    @property
    def placeholder(self):
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
        self.value = ''

    def _set_readonly(self, value):
        raise NotImplementedError('TextInput widget must define _set_readonly()')

    def _set_placeholder(self, value):
        raise NotImplementedError('TextInput widget must define _set_placeholder()')

    def _set_value(self, value):
        raise NotImplementedError('TextInput widget must define _set_value()')
