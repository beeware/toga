from .base import Widget


class TextInput(Widget):
    """ A widget get user input.

    Args:
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
        initial (str): The initial text for the input.
        placeholder (str): If no input is present this text is shown.
        readonly (bool):  Whether a user can write into the text input, defaults to `False`.
    """
    MIN_WIDTH = 100

    def __init__(
            self, id=None, style=None, factory=None,
            initial=None, placeholder=None, readonly=False):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a TextInput
        self._impl = self.factory.TextInput(interface=self)

        self.value = initial
        self.placeholder = placeholder
        self.readonly = readonly

    @property
    def readonly(self):
        """ Whether a user can write into the text input

        Returns:
            ``True`` if only read is possible.
            ``False`` if read and write is possible.
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.set_readonly(value)

    @property
    def placeholder(self):
        """ The placeholder text.

        Returns:
            The placeholder text as a ``str``.
        """
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        if value is None:
            self._placeholder = ''
        else:
            self._placeholder = str(value)
        self._impl.set_placeholder(value)
        self._impl.rehint()

    @property
    def value(self):
        """ The value of the text input field

        Returns:
            The current text of the widget as a ``str``.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if value is None:
            v = ''
        else:
            v = str(value)
        self._impl.set_value(value)
        self._impl.rehint()

    def clear(self):
        """ Clears the text of the widget """
        self.value = ''
