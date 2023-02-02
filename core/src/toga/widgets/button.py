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
        super().__init__(id=id, style=style, enabled=enabled)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        # Set all the properties
        self.text = text
        self.on_press = on_press
        self.enabled = enabled

    @property
    def text(self):
        """The text displayed on the button."""
        return self._impl.get_text()

    @text.setter
    def text(self, value):
        if value is None:
            value = ""
        else:
            value = str(value)
        self._impl.set_text(value)
        # Changing the text will probably cause the size of the button to change
        # so we need to rehint, then recompute layout.
        self._impl.rehint()
        self.refresh()

    @property
    def on_press(self):
        """The handler to invoke when the button is pressed."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = wrapped_handler(self, handler)
        self._impl.set_on_press(self._on_press)
