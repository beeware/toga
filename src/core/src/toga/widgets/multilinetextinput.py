import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class MultilineTextInput(Widget):
    """ A multi-line text input widget

    Args:
        id (str): An identifier for this widget.
        style(:obj:`Style`):  An optional style object.
            If no style is provided then a new one will be created for the widget.
        factory: Optional factory that must be able to return a implementation
            of a MulitlineTextInput Widget.
        value (str): The initial text of the widget.
        readonly (bool): Whether a user can write into the text input,
            defaults to `False`.
        placeholder (str): The placeholder text for the widget.
        on_change (``callable``): The handler to invoke when the text changes.
    """
    MIN_HEIGHT = 100
    MIN_WIDTH = 100

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,
        value=None,
        readonly=False,
        placeholder=None,
        on_change=None,
        initial=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of a MultilineTextInput
        self._impl = self.factory.MultilineTextInput(interface=self)

        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################

        # initial replaced with value
        if initial is not None:
            if value is not None:
                raise ValueError(
                    "Cannot specify both `initial` and `value`; "
                    "`initial` has been deprecated, use `value`"
                )
            else:
                warnings.warn(
                    "`initial` has been renamed `value`", DeprecationWarning
                )
            value = initial

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        # Set all the properties
        self.value = value
        self.readonly = readonly
        self.placeholder = placeholder
        self.on_change = on_change

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
        cleaned_value = '' if value is None else str(value)
        self._impl.set_value(cleaned_value)
        self._impl.rehint()

    def clear(self):
        """ Clears the text from the widget.
        """
        self.value = ''

    @property
    def on_change(self):
        """The handler to invoke when the value changes

        Returns:
            The function ``callable`` that is called on a content change.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        """Set the handler to invoke when the value is changed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the value is changed.
        """
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)
