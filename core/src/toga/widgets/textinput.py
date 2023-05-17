from typing import List, Optional

from toga.handlers import wrapped_handler

from .base import Widget


class TextInput(Widget):
    """Create a new single-line text input widget.

    Inherits from :class:`~toga.widgets.base.Widget`.
    """

    def __init__(
        self,
        id=None,
        style=None,
        value: Optional[str] = None,
        readonly: bool = False,
        placeholder: Optional[str] = None,
        on_change=None,
        on_confirm=None,
        on_gain_focus=None,
        on_lose_focus=None,
        validators: Optional[List[callable]] = None,
    ):
        """
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial content to display in the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param placeholder: The content to display as a placeholder when there
            is no user content to display.
        :param on_change: A handler that will be invoked when the the value of
            the widget changes as a result of user input.
        :param on_confirm: A handler that will be invoked when the user accepts
            the value of the input (usually by pressing Return on the keyboard).
        :param on_gain_focus: A handler that will be invoked when the widget
            gains input focus.
        :param on_lose_focus: A handler that will be invoked when the widget
            loses input focus.
        :param validators: A list of validators to run on the value of the
            input.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of the widget
        self._create()

        self.placeholder = placeholder
        self.readonly = readonly

        # Set the actual value before on_change, because we do not want
        # on_change triggered by it However, we need to prime the handler
        # property in case it is accessed.
        self._on_change = None
        self._on_confirm = None

        # Set the list of validators before we set the initial value so that
        # validation is performed on the initial value
        self.validators = validators
        self.value = value

        self.on_change = on_change
        self.on_confirm = on_confirm
        self.on_lose_focus = on_lose_focus
        self.on_gain_focus = on_gain_focus

    def _create(self):
        self._impl = self.factory.TextInput(interface=self)

    @property
    def readonly(self) -> bool:
        """Can the value of the widget be modified by the user?

        This only controls manual changes by the user (i.e., typing at the
        keyboard). Programmatic changes are permitted while the widget has
        ``readonly`` enabled.
        """
        return self._impl.get_readonly()

    @readonly.setter
    def readonly(self, value):
        self._impl.set_readonly(bool(value))

    @property
    def placeholder(self) -> str:
        """The placeholder text for the widget.

        A value of ``None`` will be interpreted and returned as an empty string.
        Any other object will be converted to a string using ``str()``.
        """
        return self._impl.get_placeholder()

    @placeholder.setter
    def placeholder(self, value):
        self._impl.set_placeholder("" if value is None else str(value))
        self.refresh()

    @property
    def value(self) -> str:
        """The text to display in the widget.

        A value of ``None`` will be interpreted and returned as an empty string.
        Any other object will be converted to a string using ``str()``.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value: str):
        if value is None:
            v = ""
        else:
            v = str(value)
        self._impl.set_value(v)
        self.refresh()

    @property
    def is_valid(self) -> bool:
        "Does the value of the widget currently pass all validators without error?"
        return self._impl.is_valid()

    @property
    def on_change(self):
        """The handler to invoke when the value of the widget changes.

        This is only invoked in response to user-generated changes.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)

    @property
    def validators(self) -> List[callable]:
        """The list of validators being used to check input on the widget.

        Changing the list of validators will cause validation to be performed.
        """
        return self._validators

    @validators.setter
    def validators(self, validators):
        replacing = hasattr(self, "_validators")
        if validators is None:
            self._validators = []
        else:
            self._validators = validators

        if replacing:
            self.validate()

    @property
    def on_gain_focus(self):
        """The handler to invoke when the widget gains input focus."""
        return self._on_gain_focus

    @on_gain_focus.setter
    def on_gain_focus(self, handler):
        self._on_gain_focus = wrapped_handler(self, handler)

    @property
    def on_lose_focus(self):
        """The handler to invoke when the widget loses input focus."""
        return self._on_lose_focus

    @on_lose_focus.setter
    def on_lose_focus(self, handler):
        self._on_lose_focus = wrapped_handler(self, handler)

    def validate(self) -> bool:
        """Validate the current value of the widget.

        If a problem is found, the widget will be put into an error state.

        :returns: ``True`` if the input is valid; ``False`` otherwise.
        """
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

    @property
    def on_confirm(self):
        """The handler to invoke when the user accepts the value of the widget,
        usually by pressing return/enter on the keyboard.
        """
        return self._on_confirm

    @on_confirm.setter
    def on_confirm(self, handler):
        if not getattr(self._impl, "IMPLEMENTS_ON_CONFIRM", True):  # pragma: no cover
            self.factory.not_implemented("TextInput.on_confirm()")
        self._on_confirm = wrapped_handler(self, handler)
