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
        validators (list): list of validators to run on the value of the text box. Should
            return None is value is valid and an error message if not.
        on_change (``callable``): The handler to invoke when the text changes.
        on_gain_focus (:obj:`callable`): Function to execute when get focused.
        on_lose_focus (:obj:`callable`): Function to execute when lose focus.
    """
    MIN_WIDTH = 100

    def __init__(
        self,
        id=None,
        style=None,
        factory=None,
        initial=None,
        placeholder=None,
        readonly=False,
        on_change=None,
        on_gain_focus=None,
        on_lose_focus=None,
        validators=None
    ):
        super().__init__(id=id, style=style, factory=factory)

        # Create a platform specific implementation of the widget
        self._create()

        self.on_change = on_change
        self.placeholder = placeholder
        self.readonly = readonly

        # Set the actual value after on_change, as it may trigger change events, etc.
        self.value = initial
        self.validators = validators
        self.on_lose_focus = on_lose_focus
        self.on_gain_focus = on_gain_focus

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
    def validators(self):
        return self._validators

    @validators.setter
    def validators(self, validators):
        if validators is None:
            self._validators = []
        else:
            self._validators = validators
        self.validate()

    @property
    def on_gain_focus(self):
        """The handler to invoke when the widget get focus.

        Returns:
            The function ``callable`` that is called on widget focus gain.
        """
        return self._on_gain_focus

    @on_gain_focus.setter
    def on_gain_focus(self, handler):
        self._on_gain_focus = wrapped_handler(self, handler)
        self._impl.set_on_gain_focus(self._on_gain_focus)

    @property
    def on_lose_focus(self):
        """The handler to invoke when the widget lose focus.

        Returns:
            The function ``callable`` that is called on widget focus loss.
        """
        return self._on_lose_focus

    @on_lose_focus.setter
    def on_lose_focus(self, handler):
        self._on_lose_focus = wrapped_handler(self, handler)
        self._impl.set_on_lose_focus(self._on_lose_focus)

    def validate(self):
        error_message = None
        for validator in self.validators:
            if error_message is None:
                error_message = validator(self.value)

        if error_message is None:
            self._impl.clear_error()
            return True
        else:
            self._impl.set_error(error_message)
            return False
