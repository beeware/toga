import warnings

from toga.handlers import wrapped_handler

from .base import Widget

# BACKWARDS COMPATIBILITY: a token object that can be used to differentiate
# between an explicitly provided ``None``, and a unspecified value falling
# back to a default.
NOT_PROVIDED = object()


class Button(Widget):
    """A clickable button widget.

    Args:
        text (str): Text to be shown on the button.
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        on_press (:obj:`callable`): Function to execute when pressed.
        enabled (bool): Whether or not interaction with the button is possible,
            defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not
            needed)
    """

    def __init__(
            self,
            text=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
                                # can be removed when the handling for
                                # `label` is removed
            id=None,
            style=None,
            on_press=None,
            enabled=True,
            factory=None,
            label=None,  # DEPRECATED!
    ):
        super().__init__(id=id, style=style, enabled=enabled, factory=factory)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################
        # When deleting this block, also delete the NOT_PROVIDED
        # placeholder, and replace it's usage in default values.

        # label replaced with text
        if label is not None:
            if text is not NOT_PROVIDED:
                raise ValueError(
                    "Cannot specify both `label` and `text`; "
                    "`label` has been deprecated, use `text`"
                )
            else:
                warnings.warn(
                    "Button.label has been renamed Button.text", DeprecationWarning
                )
                text = label
        elif text is NOT_PROVIDED:
            # This would be raised by Python itself; however, we need to use a placeholder
            # value as part of the migration from text->value.
            raise TypeError("Button.__init__ missing 1 required positional argument: 'text'")

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        # Set all the properties
        self.text = text
        self.on_press = on_press
        self.enabled = enabled

    @property
    def text(self):
        """
        Returns:
            The button text as a ``str``
        """
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            self._text = ''
        else:
            self._text = str(value)
        self._impl.set_text(value)
        self._impl.rehint()

    @property
    def on_press(self):
        """The handler to invoke when the button is pressed.

        Returns:
            The function ``callable`` that is called on button press.
        """
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        """Set the handler to invoke when the button is pressed.

        Args:
            handler (:obj:`callable`): The handler to invoke when the button is pressed.
        """
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################
    # label replaced with text
    @property
    def label(self):
        """ Button text.

        **DEPRECATED: renamed as text**

        Returns:
            The button text as a ``str``
        """
        warnings.warn(
            "Button.label has been renamed Button.text", DeprecationWarning
        )
        return self.text

    @label.setter
    def label(self, label):
        warnings.warn(
            "Button.label has been renamed Button.text", DeprecationWarning
        )
        self.text = label
    ######################################################################
    # End backwards compatibility.
    ######################################################################
