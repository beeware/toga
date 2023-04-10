from toga.handlers import wrapped_handler

from .base import Widget


class Switch(Widget):
    def __init__(
        self,
        text,
        id=None,
        style=None,
        on_change=None,
        value=False,
        enabled=True,
    ):
        """Create a new Switch widget.

        Inherits from :class:`~toga.widgets.base.Widget`.

        :param text: The text to display beside the switch.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param on_change: A handler that will be invoked when the switch changes
            value.
        :param enabled: Is the switch enabled (i.e., can it be pressed?).
            Optional; by default, switches are created in an enabled state.
        """
        super().__init__(id=id, style=style)

        self._impl = self.factory.Switch(interface=self)

        self.text = text

        # Set a dummy handler before installing the actual on_change, because we do not want
        # on_change triggered by the initial value being set
        self.on_change = None
        self.value = value

        self.on_change = on_change

        self.enabled = enabled

    @property
    def text(self):
        """The text label for the Switch.

        ``None``, and the Unicode codepoint U+200B (ZERO WIDTH SPACE), will be
        interpreted and returned as an empty string. Any other object will be
        converted to a string using ``str()``.

        Only one line of text can be displayed. Any content after the first
        newline will be ignored.
        """
        return self._impl.get_text()

    @text.setter
    def text(self, value):
        if value is None or value == "\u200B":
            value = ""
        else:
            # Switch text can't include line breaks. Strip any content
            # after a line break (if provided)
            value = str(value).split("\n")[0]

        self._impl.set_text(value)
        self.refresh()

    @property
    def on_change(self):
        """The handler to invoke when the value of the switch changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler):
        self._on_change = wrapped_handler(self, handler)

    @property
    def value(self):
        """The current state of the switch, as a Boolean.

        Any non-Boolean value will be converted to a Boolean.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value):
        self._impl.set_value(bool(value))

    def toggle(self):
        """Reverse the current value of the switch."""
        self.value = not self.value
