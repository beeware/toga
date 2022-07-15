import warnings

from toga.handlers import wrapped_handler

from .base import Widget


class Switch(Widget):
    """
    Switch widget, a clickable button with two stable states, True (on, checked)
        and False (off, unchecked).

    Args:
        text (str): Text to be shown next to the switch.
        id (str): AN identifier for this widget.
        style (:obj:`Style`): An optional style object.
            If no style is provided then a new one will be created for the widget.
        on_change (``callable``): Function to execute when pressed.
        value (bool): Current on or off state of the switch.
        enabled (bool): Whether or not interaction with the button is possible, defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(
            self,
            text,
            id=None,
            style=None,
            on_change=None,
            on_toggle=None,  # DEPRECATED!
            is_on=None,
            value=False,
            enabled=True,
            factory=None,
    ):
        super().__init__(id=id, style=style, factory=factory)

        self._impl = self.factory.Switch(interface=self)

        self.text = text
        if on_toggle:
            self.on_toggle = on_toggle
        else:
            self.on_change = on_change
        if is_on is not None:
            self.is_on = is_on
        else:
            self.value = value
        self.enabled = enabled

    @property
    def text(self):
        """ Accompanying text label of the Switch.

        Returns:
            The label text of the widget as a ``str``.
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
    def on_change(self):
        """ The callable function for when the switch is pressed

        Returns:
            The ``callable`` on_change function.
        """
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)
        self._impl.set_on_change(self._on_change)

    @property
    def on_toggle(self):
        """ The callable function for when the switch is pressed

        **DEPRECATED: renamed as on_change**

        Returns:
            The ``callable`` on_toggle function.
        """
        warnings.warn(
            "Switch.on_toggle has been renamed Switch.on_change", DeprecationWarning
        )
        return self.on_change

    @on_toggle.setter
    def on_toggle(self, handler):
        warnings.warn(
            "Switch.on_toggle has been renamed Switch.on_change", DeprecationWarning
        )
        self.on_change = handler

    @property
    def is_on(self):
        """ Button Off/On state.

        **DEPRECATED: renamed as value**

        Returns:
            ``True`` if on and ``False`` if the switch is off.
        """
        warnings.warn(
            "Switch.is_on has been renamed Switch.value", DeprecationWarning
        )
        return self.value

    @is_on.setter
    def is_on(self, value):
        warnings.warn(
            "Switch.is_on has been renamed Switch.value", DeprecationWarning
        )
        self.value = value

    @property
    def value(self):
        """ Button Off/On state.

        Returns:
            ``True`` if on and ``False`` if the switch is off.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        if not isinstance(value, bool):
            raise ValueError("Switch.value can only be set to true or false")
        self._impl.set_value(value)

    def toggle(self):
        """Reverse the value of `Switch.value` property from true to false and
        vice versa.
        """
        self.value = not self.value

    @property
    def label(self):
        """ Button Off/On state.

        **DEPRECATED: renamed as text**

        Returns:
            ``True`` if on and ``False`` if the switch is off.
        """
        warnings.warn(
            "Switch.label has been renamed Switch.text", DeprecationWarning
        )
        return self.text

    @label.setter
    def label(self, label):
        warnings.warn(
            "Switch.label has been renamed Switch.text", DeprecationWarning
        )
        self.text = label
