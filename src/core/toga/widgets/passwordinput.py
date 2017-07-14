from .base import Widget


class PasswordInput(Widget):
    def __init__(
            self, id=None, style=None, factory=None,
            initial=None, placeholder=None, readonly=False):
        """ Instantiate a new instance of the password input widget

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
        """
        super().__init__(id=id, style=style, factory=factory)


        # Create a platform specific implementation of a PasswordInput
        self._impl = self.factory.PasswordInput(interface=self)

        self.value = initial
        self.placeholder = placeholder
        self.readonly = readonly

    @property
    def readonly(self):
        """ Whether a user can write into the password input

        :rtype: ``bool``
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.set_readonly(value)

    @property
    def placeholder(self):
        """ The placeholder text is the displayed before the user input something.

        Returns:
            The placeholder text (str) of the widget.
        """
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        if value is None:
            self._placeholder = ''
        else:
            self._placeholder = str(value)
        self._impl.set_placeholder(value)
        self.rehint()

    @property
    def value(self):
        """ The value of the text input field.

        Returns:
            value (str): The text of the password input widget.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if value is None:
            v = ''
        else:
            v = str(value)
        self._impl.set_value(v)
        self.rehint()

    def clear(self):
        """ Clear the value
        """
        self.value = ''
