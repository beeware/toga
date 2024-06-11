from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from toga.widgets.base import Widget


class TogaApplicator:
    """Apply styles to a Toga widget."""

    def __init__(self, widget: Widget):
        self.widget = widget

    def refresh(self) -> None:
        # print("RE-EVALUATE LAYOUT", self.widget)
        self.widget.refresh()

    def set_bounds(self) -> None:
        # print("  APPLY LAYOUT", self.widget, self.widget.layout)
        self.widget._impl.set_bounds(
            self.widget.layout.absolute_content_left,
            self.widget.layout.absolute_content_top,
            self.widget.layout.content_width,
            self.widget.layout.content_height,
        )
        for child in self.widget.children:
            child.applicator.set_bounds()

    def set_text_alignment(self, alignment: str) -> None:
        self.widget._impl.set_alignment(alignment)

    def set_hidden(self, hidden: bool) -> None:
        self.widget._impl.set_hidden(hidden)
        for child in self.widget.children:
            # If the parent is hidden, then so are all children. However, if the
            # parent is visible, then the child's explicit visibility style is
            # taken into account. This visibility cascades into any
            # grandchildren.
            #
            # parent hidden child hidden style child final hidden state
            # ============= ================== ========================
            # True          True               True
            # True          False              True
            # False         True               True
            # False         False              False
            child.applicator.set_hidden(hidden or child.style._hidden)

    def set_font(self, font: object) -> None:
        # Changing the font of a widget can make the widget change size,
        # which in turn means we need to do a re-layout
        self.widget._impl.set_font(font)
        self.widget.refresh()

    def set_color(self, color: object) -> None:
        self.widget._impl.set_color(color)

    def set_background_color(self, color: object) -> None:
        self.widget._impl.set_background_color(color)
