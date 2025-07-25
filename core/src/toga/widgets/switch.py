from __future__ import annotations

from typing import Any, Protocol

import toga
from toga.handlers import wrapped_handler

from .base import StyleT, Widget


class OnChangeHandler(Protocol):
    def __call__(self, widget: Switch, **kwargs: Any) -> None:
        """A handler to invoke when the value is changed.

        :param widget: The Switch that was changed.
        :param kwargs: Ensures compatibility with arguments added in future versions.
        """


class Switch(Widget):
    def __init__(
        self,
        text: str,
        id: str | None = None,
        style: StyleT | None = None,
        on_change: toga.widgets.switch.OnChangeHandler | None = None,
        value: bool = False,
        enabled: bool = True,
        **kwargs,
    ):
        """Create a new Switch widget.

        :param text: The text to display beside the switch.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial value for the switch.
        :param on_change: A handler that will be invoked when the switch changes
            value.
        :param enabled: Is the switch enabled (i.e., can it be pressed?).
            Optional; by default, switches are created in an enabled state.
        :param kwargs: Initial style properties.
        """
        super().__init__(id, style, **kwargs)

        self.text = text

        # Set a dummy handler before installing the actual on_change, because we do not
        # want on_change triggered by the initial value being set
        self.on_change = None
        self.value = value

        self.on_change = on_change

        self.enabled = enabled

    def _create(self) -> Any:
        return self.factory.Switch(interface=self)

    @property
    def text(self) -> str:
        """The text label for the Switch.

        ``None``, and the Unicode codepoint U+200B (ZERO WIDTH SPACE), will be
        interpreted and returned as an empty string. Any other object will be
        converted to a string using ``str()``.

        Only one line of text can be displayed. Any content after the first
        newline will be ignored.
        """
        return self._impl.get_text()

    @text.setter
    def text(self, value: object) -> None:
        if value is None or value == "\u200b":
            value = ""
        else:
            # Switch text can't include line breaks. Strip any content
            # after a line break (if provided)
            value = str(value).split("\n")[0]

        self._impl.set_text(value)
        self.refresh()

    @property
    def on_change(self) -> OnChangeHandler:
        """The handler to invoke when the value of the switch changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler: toga.widgets.switch.OnChangeHandler) -> None:
        self._on_change = wrapped_handler(self, handler)

    @property
    def value(self) -> bool:
        """The current state of the switch, as a Boolean.

        Any non-Boolean value will be converted to a Boolean.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value: object) -> None:
        self._impl.set_value(bool(value))

    def toggle(self) -> None:
        """Reverse the current value of the switch."""
        self.value = not self.value
