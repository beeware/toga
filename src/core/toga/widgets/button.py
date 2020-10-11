from toga.handlers import wrapped_handler

from .base import Widget


class Button(Widget):
    """A clickable button widget.

    Args:
        label (str): Text to be shown on the button.
        id (str): An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no style is provided then
            a new one will be created for the widget.
        on_press (:obj:`callable`): Function to execute when pressed.
        on_focus_gain (:obj:`callable`): Function to execute when get focused.
        on_focus_loss (:obj:`callable`): Function to execute when lose focus.
        enabled (bool): Whether or not interaction with the button is possible, defaults to `True`.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional & normally not needed)
    """

    def __init__(
            self,
            label,
            id=None,
            style=None,
            on_press=None,
            on_focus_gain=None,
            on_focus_loss=None,
            enabled=True,
            factory=None
    ):
        super().__init__(
            id=id,
            style=style,
            enabled=enabled,
            on_focus_gain=on_focus_gain,
            on_focus_loss=on_focus_loss,
            factory=factory,
        )

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        # Set all the properties
        self.label = label
        self.on_press = on_press
        self.on_focus_gain = on_focus_gain
        self.on_focus_loss = on_focus_loss
        self.enabled = enabled

    @property
    def label(self):
        """
        Returns:
            The button label as a ``str``
        """
        return self._label

    @label.setter
    def label(self, value):
        if value is None:
            self._label = ''
        else:
            self._label = str(value)
        self._impl.set_label(value)
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
