from __future__ import annotations

from toga.constants import Direction

from .base import Widget


class SplitContainer(Widget):
    HORIZONTAL = Direction.HORIZONTAL
    VERTICAL = Direction.VERTICAL

    def __init__(
        self,
        id=None,
        style=None,
        direction: Direction = Direction.VERTICAL,
        content: tuple[Widget | tuple[Widget, int], Widget | tuple[Widget, int]] = (
            None,
            None,
        ),
    ):
        """Create a new SplitContainer.

        Inherits from :class:`toga.Widget`.

        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param direction: The direction in which the divider will be drawn. Either
            :attr:`~toga.constants.Direction.HORIZONTAL` or
            :attr:`~toga.constants.Direction.VERTICAL`; defaults to
            :attr:`~toga.constants.Direction.VERTICAL`
        :param content: The content that will fill the panels of the SplitContainer. A
            tuple with 2 elements; each item in the tuple is either:

            * A tuple consisting of a widget and the initial flex value to apply to
              that widget in the split.
            * A widget. The widget will be given a flex value of 1.

        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of a SplitContainer
        self._impl = self.factory.SplitContainer(interface=self)

        self.content = content
        self.direction = direction

    @property
    def enabled(self) -> bool:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        SplitContainer widgets cannot be disabled; this property will always return
        True; any attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value):
        pass

    def focus(self):
        "No-op; SplitContainer cannot accept input focus"
        pass

    @property
    def content(self) -> tuple[Widget, Widget]:
        """The widgets displayed in the SplitContainer.

        When retrieved, only the list of widgets is returned.

        When setting the value, the list must have exactly 2 elements; each item in the
        list can be either:

        * A tuple consisting of a widget and the initial flex value to apply to that
          widget in the split.
        * A widget. The widget will be given a flex value of 1.

        """
        return self._content

    @content.setter
    def content(
        self, content: tuple[Widget | tuple[Widget, int], Widget | tuple[Widget, int]]
    ):
        try:
            if len(content) != 2:
                raise TypeError()
        except TypeError:
            raise ValueError(
                "SplitContainer content must be a sequence with exactly 2 elements"
            )

        _content = []
        flex = []
        for item in content:
            if isinstance(item, tuple):
                if len(item) == 2:
                    widget, flex_value = item
                    if flex_value <= 0:
                        raise ValueError(
                            "The flex value for an item in a SplitContainer must be >0"
                        )
                else:
                    raise ValueError(
                        "An item in SplitContainer content must be a 2-tuple "
                        "containing the widget, and the flex weight to assign to that "
                        "widget."
                    )
            else:
                widget = item
                flex_value = 1

            _content.append(widget)
            flex.append(flex_value)

            if widget:
                widget.app = self.app
                widget.window = self.window

        self._impl.set_content(
            tuple(w._impl if w is not None else None for w in _content),
            flex,
        )
        self._content = tuple(_content)
        self.refresh()

    @Widget.app.setter
    def app(self, app):
        # Invoke the superclass property setter
        Widget.app.fset(self, app)

        # Also assign the app to the content in the container
        for content in self.content:
            if content:
                content.app = app

    @Widget.window.setter
    def window(self, window):
        # Invoke the superclass property setter
        Widget.window.fset(self, window)

        # Also assign the window to the content in the container
        for content in self._content:
            if content:
                content.window = window

    @property
    def direction(self) -> Direction:
        """The direction of the split"""
        return self._impl.get_direction()

    @direction.setter
    def direction(self, value):
        self._impl.set_direction(value)
        self.refresh()
