from .base import Widget


class PasswordInput(Widget):
    """ This widgets behaves like a TextInput but does not reveal what text is entered.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        initial (str): The initial text that is displayed before the user inputs anything.
        placeholder (str): The text that is displayed if no input text is present.
        readonly (bool): Whether a user can write into the text input, defaults to `False`.
    """
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, factory=None,
                initial=None, placeholder=None, readonly=False):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a PasswordInput
        self._impl = self.factory.PasswordInput(interface=self)

        self.value = initial
        self.placeholder = placeholder
        self.readonly = readonly

    @property
    def readonly(self):
        """ Whether a user can write into the password input

        Returns:
            ``True`` if the user can only read,
            ``False`` if the user can read and write into the input.
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
        self._impl.set_placeholder(self._placeholder)
        self._impl.rehint()

    @property
    def value(self):
        """ The value of the text input field.

        Returns:
            The text as a ``str`` of the password input widget.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if value is None:
            v = ''
        else:
            v = str(value)
        self._impl.set_value(v)
        self._impl.rehint()

    def clear(self):
        """ Clears the input field of the widget.
        """
        self.value = ''
