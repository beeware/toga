from .base import Widget


class MultilineTextInput(Widget):
    """ A multi-line text input widget

    Args:
        id (str): An identifier for this widget.
        style(:class:`colosseum.CSSNode`):  An optional style object.
            If no style is provided then a new one will be created for the widget.
        factory: Optional factory that must be able to return a implementation
            of a MulitlineTextInput Widget.
        initial (str): The initial text of the widget.
    """

    def __init__(self, id=None, style=None, factory=None,
                 initial=None):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.MultilineTextInput(interface=self)
        self.value = initial

    @property
    def value(self):
        """ The value of the multiline text input field.

        Returns:
            The text of the Widget as a ``str``.
        """
        return self._value

    @value.setter
    def value(self, value):
        self._value = '' if value is None else str(value)
        self._impl.set_value(self._value)
        self.rehint()

    def clear(self):
        """ Clears the text from the widget.
        """
        self.value = ''
