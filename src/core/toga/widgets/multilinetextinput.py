from .base import Widget


class MultilineTextInput(Widget):
    """ A multi-line text input widget

    Args:
        id (str): An identifier for this widget.
        style(:obj:`Style`):  An optional style object.
            If no style is provided then a new one will be created for the widget.
        factory: Optional factory that must be able to return a implementation
            of a MulitlineTextInput Widget.
        initial (str): The initial text of the widget.
        readonly (bool): Whether a user can write into the text input,
            defaults to `False`.
        placeholder (str): The placeholder text for the widget.
    """
    MIN_HEIGHT = 100
    MIN_WIDTH = 100

    def __init__(self, id=None, style=None, factory=None,
                 initial=None, readonly=False, placeholder=None):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.MultilineTextInput(interface=self)
        self.value = initial
        self.readonly = readonly
        self.placeholder = placeholder

    @property
    def placeholder(self):
        """ The placeholder text

        Returns:
            The placeholder text as a `str``.
        """
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = '' if value is None else str(value)
        self._impl.set_placeholder(self._placeholder)

    @property
    def readonly(self):
        """ Whether a user can write into the text input

        Returns:
            `True` if the user can only read, `False` if the user can read and write the text.
        """
        return self._readonly

    @readonly.setter
    def readonly(self, value):
        self._readonly = value
        self._impl.set_readonly(value)

    @property
    def value(self):
        """ The value of the multi line text input field.

        Returns:
            The text of the Widget as a ``str``.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        self._value = '' if value is None else str(value)
        self._impl.set_value(self._value)
        self._impl.rehint()

    def clear(self):
        """ Clears the text from the widget.
        """
        self.value = ''
