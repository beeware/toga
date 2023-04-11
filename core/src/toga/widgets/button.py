from toga.handlers import wrapped_handler

from .base import Widget


class Button(Widget):
    def __init__(
        self,
        text,
        id=None,
        style=None,
        on_press=None,
        enabled=True,
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
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        # Set a dummy handler before installing the actual on_press, because we do not want
        # on_press triggered by the initial value being set
        self.on_press = None
        self.text = text

        self.on_press = on_press
        self.enabled = enabled

    @property
    def text(self):
        """The text displayed on the button.

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
            # Button text can't include line breaks. Strip any content
            # after a line break (if provided)
            value = str(value).split("\n")[0]

        self._impl.set_text(value)
        self.refresh()

    @property
    def on_press(self):
        """The handler to invoke when the button is pressed."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = wrapped_handler(self, handler)
