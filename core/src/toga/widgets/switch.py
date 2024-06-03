from __future__ import annotations

from typing import Protocol, Union

from toga.handlers import HandlerGeneratorReturnT, WrappedHandlerT, wrapped_handler
from toga.types import TypeAlias

from .base import StyleT, Widget


class OnChangeHandlerSync(Protocol):
    def __call__(self, /) -> object:
        """A handler to invoke when the value is changed."""


class OnChangeHandlerAsync(Protocol):
    async def __call__(self, /) -> object:
        """Async definition of :any:`OnChangeHandlerSync`."""


class OnChangeHandlerGenerator(Protocol):
    def __call__(self, /) -> HandlerGeneratorReturnT[object]:
        """Generator definition of :any:`OnChangeHandlerSync`."""


OnChangeHandlerT: TypeAlias = Union[
    OnChangeHandlerSync, OnChangeHandlerAsync, OnChangeHandlerGenerator
]


class Switch(Widget):
    def __init__(
        self,
        text: str,
        id: str | None = None,
        style: StyleT | None = None,
        on_change: OnChangeHandlerT | None = None,
        value: bool = False,
        enabled: bool = True,
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
        if value is None or value == "\u200B":
            value = ""
        else:
            # Switch text can't include line breaks. Strip any content
            # after a line break (if provided)
            value = str(value).split("\n")[0]

        self._impl.set_text(value)
        self.refresh()

    @property
    def on_change(self) -> WrappedHandlerT:
        """The handler to invoke when the value of the switch changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler: OnChangeHandlerT) -> None:
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
