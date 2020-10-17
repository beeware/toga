from toga.handlers import wrapped_handler

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
        on_change (Callable): Method to be called when text is changed in text box
        validator (Callable): Validator to run on the value of the text box. Should
            return None is value is valid and an error message if not.
    """
    MIN_WIDTH = 100

    def __init__(
            self, id=None, style=None, factory=None,
            initial=None, placeholder=None, readonly=False, on_change=None,
            validator=None
    ):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of the widget
        self._create()

        self.on_change = on_change
        self.placeholder = placeholder
        self.readonly = readonly

        # Set the actual value after on_change, as it may trigger change events, etc.
        self.value = initial
        self.validator = validator

    def _create(self):
        self._impl = self.factory.TextInput(interface=self)

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
        self._impl.set_value(v)

    def clear(self):
        """ Clears the text of the widget """
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

    @property
    def validator(self):
        return self._validator

    @validator.setter
    def validator(self, validator):
        self._validator = validator
        self.validate()

    def validate(self):
        if self.validator is None:
            error_message = None
        else:
            error_message = self.validator(self.value)

        if error_message is None:
            self._impl.clear_error()
            return True
        else:
            self._impl.set_error(error_message)
            return False

    def is_valid(self):
        if self.validator is None:
            return True
        return self.validator(self.value) is None
