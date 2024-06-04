from __future__ import annotations

from collections.abc import Iterable

from .base import StyleT, Widget


class Box(Widget):
    _MIN_WIDTH = 0
    _MIN_HEIGHT = 0

    def __init__(
        self,
        id: str | None = None,
        style: StyleT | None = None,
        children: Iterable[Widget] | None = None,
    ):
        """Create a new Box container widget.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        :param children: An optional list of children for to add to the Box.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a Box
        self._impl = self.factory.Box(interface=self)

        # Children need to be added *after* the impl has been created.
        self._children: list[Widget] = []
        if children is not None:
            self.add(*children)

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        Box widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: bool) -> None:
        pass

    def focus(self) -> None:
        """No-op; Box cannot accept input focus."""
        pass
