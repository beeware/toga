from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

import toga
from toga.handlers import wrapped_handler

from .base import Widget

if TYPE_CHECKING:
    from toga.icons import IconContent


class OnPressHandler(Protocol):
    def __call__(self, widget: Button, **kwargs: Any) -> None:
        """A handler that will be invoked when a button is pressed.

        .. note::
            ``**kwargs`` ensures compatibility with additional arguments
            introduced in future versions.

        :param widget: The button that was pressed.
        """
        ...


class Button(Widget):
    def __init__(
        self,
        text: str | None = None,
        icon: IconContent | None = None,
        id: str | None = None,
        style=None,
        on_press: OnPressHandler | None = None,
        enabled: bool = True,
    ):
        """Create a new button widget.

        :param text: The text to display on the button.
        :param icon: The icon to display on the button. Can be specified as any valid
            :any:`icon content <IconContent>`.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param on_press: A handler that will be invoked when the button is pressed.
        :param enabled: Is the button enabled (i.e., can it be pressed?). Optional; by
            default, buttons are created in an enabled state.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a Button
        self._impl = self.factory.Button(interface=self)

        # Set a dummy handler before installing the actual on_press, because we do not want
        # on_press triggered by the initial value being set
        self.on_press = None

        # Set the content of the button - either an icon, or text, but not both.
        if icon:
            if text is not None:
                raise ValueError("Cannot specify both text and an icon")
            else:
                self.icon = icon
        else:
            self.text = text

        self.on_press = on_press
        self.enabled = enabled

    @property
    def text(self) -> str:
        """The text displayed on the button.

        ``None``, and the Unicode codepoint U+200B (ZERO WIDTH SPACE), will be
        interpreted and returned as an empty string. Any other object will be converted
        to a string using ``str()``.

        Only one line of text can be displayed. Any content after the first newline will
        be ignored.

        If the button is currently displaying an icon, and text is assigned, the icon
        will be replaced by the new text.

        If the button is currently displaying an icon, the empty string will be
        returned.
        """
        return self._impl.get_text()

    @text.setter
    def text(self, value: str | None) -> None:
        if value is None or value == "\u200B":
            value = ""
        else:
            # Button text can't include line breaks. Strip any content
            # after a line break (if provided)
            value = str(value).split("\n")[0]

        self._impl.set_text(value)
        self._impl.set_icon(None)
        self.refresh()

    @property
    def icon(self) -> toga.Icon | None:
        """The icon displayed on the button.

        Can be specified as any valid :any:`icon content <IconContent>`.

        If the button is currently displaying text, and an icon is assigned, the text
        will be replaced by the new icon.

        If ``None`` is assigned as an icon, the button will become a text button with an
        empty label.

        Returns ``None`` if the button is currently displaying text.
        """
        return self._impl.get_icon()

    @icon.setter
    def icon(self, value: IconContent | None) -> None:
        if isinstance(value, toga.Icon):
            icon = value
            text = ""
        elif value is None:
            if self.icon is None:
                # Already a null icon; nothing changes.
                return
            else:
                icon = None
                text = self._impl.get_text()
        else:
            icon = toga.Icon(value)
            text = ""

        self._impl.set_icon(icon)
        self._impl.set_text(text)
        self.refresh()

    @property
    def on_press(self) -> OnPressHandler:
        """The handler to invoke when the button is pressed."""
        return self._on_press

    @on_press.setter
    def on_press(self, handler):
        self._on_press = wrapped_handler(self, handler)
