from __future__ import annotations

from typing import Protocol, Union

from toga.handlers import HandlerGeneratorReturnT, WrappedHandlerT, wrapped_handler
from toga.style import Pack
from toga.types import TypeAlias

from .base import Widget


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


class MultilineTextInput(Widget):
    def __init__(
        self,
        id: str | None = None,
        style: Pack | None = None,
        value: str | None = None,
        readonly: bool = False,
        placeholder: str | None = None,
        on_change: OnChangeHandlerT | None = None,
    ):
        """Create a new multi-line text input widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param value: The initial content to display in the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param placeholder: The content to display as a placeholder when
            there is no user content to display.
        :param on_change: A handler that will be invoked when the value of
            the widget changes.
        """

        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a MultilineTextInput
        self._impl = self.factory.MultilineTextInput(interface=self)

        # Set a dummy handler before installing the actual on_change, because we do not want
        # on_change triggered by the initial value being set
        self.on_change = None  # type: ignore[assignment]
        self.value = value  # type: ignore[assignment]

        # Set all the properties
        self.readonly = readonly
        self.placeholder = placeholder  # type: ignore[assignment]
        self.on_change = on_change  # type: ignore[assignment]

    @property
    def placeholder(self) -> str:
        """The placeholder text for the widget.

        A value of ``None`` will be interpreted and returned as an empty string.
        Any other object will be converted to a string using ``str()``.
        """
        return self._impl.get_placeholder()

    @placeholder.setter
    def placeholder(self, value: object) -> None:
        self._impl.set_placeholder("" if value is None else str(value))
        self.refresh()

    @property
    def readonly(self) -> bool:
        """Can the value of the widget be modified by the user?

        This only controls manual changes by the user (i.e., typing at the
        keyboard). Programmatic changes are permitted while the widget has
        ``readonly`` enabled.
        """
        return self._impl.get_readonly()

    @readonly.setter
    def readonly(self, value: object) -> None:
        self._impl.set_readonly(bool(value))

    @property
    def value(self) -> str:
        """The text to display in the widget.

        A value of ``None`` will be interpreted and returned as an empty string.
        Any other object will be converted to a string using ``str()``.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value: object) -> None:
        self._impl.set_value("" if value is None else str(value))
        self.refresh()

    def scroll_to_bottom(self) -> None:
        """Scroll the view to make the bottom of the text field visible."""
        self._impl.scroll_to_bottom()

    def scroll_to_top(self) -> None:
        """Scroll the view to make the top of the text field visible."""
        self._impl.scroll_to_top()

    @property
    def on_change(self) -> WrappedHandlerT:
        """The handler to invoke when the value of the widget changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler: OnChangeHandlerT) -> None:
        self._on_change = wrapped_handler(self, handler)
