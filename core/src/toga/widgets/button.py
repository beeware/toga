import warnings

from toga.handlers import wrapped_handler

from .base import Widget

# BACKWARDS COMPATIBILITY: a token object that can be used to differentiate
# between an explicitly provided ``None``, and a unspecified value falling
# back to a default.
NOT_PROVIDED = object()


class Button(Widget):
    def __init__(
        self,
        text=NOT_PROVIDED,  # BACKWARDS COMPATIBILITY: The default value
        # can be removed when the handling for `label` is removed
        id=None,
        style=None,
        on_press=None,
        enabled=True,
        factory=None,  # DEPRECATED!
        label=None,  # DEPRECATED!
    ):
        """Create a new button widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param text: The text to display on the button.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param on_press: A handler that will be invoked when the button is
            pressed.
        :param enabled: Is the button enabled (i.e., can it be pressed?).
            Optional; by default, buttons are created in an enabled state.
        :param factory: *Deprecated*
        :param label: *Deprecated*; renamed ``text``.
        """
        super().__init__(id=id, style=style, enabled=enabled)

        ######################################################################
        # 2022-09: Backwards compatibility
        ######################################################################
        # factory no longer used
        if factory:
            warnings.warn("The factory argument is no longer used.", DeprecationWarning)
        ######################################################################
        # End backwards compatibility.
        ######################################################################

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        ##################################################################
        # 2022-07: Backwards compatibility
        ##################################################################
        # When deleting this block, also delete the NOT_PROVIDED
        # placeholder, and replace its usage in default values.

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
            raise TypeError(
                "Button.__init__ missing 1 required positional argument: 'text'"
            )

        ##################################################################
        # End backwards compatibility.
        ##################################################################

        # Set all the properties
        self.text = text
        self.on_press = on_press
        self.enabled = enabled

    @property
    def text(self):
        """The text displayed on the button."""
        return self._text

    @text.setter
    def text(self, value):
        if value is None:
            self._text = ""
        else:
            self._text = str(value)
        self._impl.set_text(value)
        self._impl.rehint()

    @property
    def on_press(self):
        """The handler to invoke when the button is pressed."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)

    ######################################################################
    # 2022-07: Backwards compatibility
    ######################################################################
    # label replaced with text
    @property
    def label(self):
        """The text label displayed on the button.

        :deprecated: :py:attr:`label` has been renamed :py:attr:`~text`.
        """

        warnings.warn("Button.label has been renamed Button.text", DeprecationWarning)
        return self.text

    @label.setter
    def label(self, label):
        warnings.warn("Button.label has been renamed Button.text", DeprecationWarning)
        self.text = label

    ######################################################################
    # End backwards compatibility.
    ######################################################################
