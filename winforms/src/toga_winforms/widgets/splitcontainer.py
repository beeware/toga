from System.Windows.Forms import (
    BorderStyle,
    Orientation,
    SplitContainer as NativeSplitContainer,
)

from toga.constants import Direction

from ..container import Container
from ..libs.wrapper import WeakrefCallable
from .base import Widget


class SplitContainer(Widget):
    def create(self):
        self.native = NativeSplitContainer()
        self.native.SplitterMoved += WeakrefCallable(self.winforms_splitter_moved)

        # Despite what the BorderStyle documentation says, there is no border by default
        # (at least on Windows 10), which would make the split bar invisible.
        self.native.BorderStyle = BorderStyle.Fixed3D

        self.panels = (Container(self.native.Panel1), Container(self.native.Panel2))
        self.pending_position = None

    def winforms_splitter_moved(self, sender, event):
        self.resize_content()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        force_refresh = False
        if self.pending_position:
            self.set_position(self.pending_position)
            self.pending_position = None
            force_refresh = True  # Content has changed

        self.resize_content(force_refresh=force_refresh)

    def set_content(self, content, flex):
        # In case content moves from one panel to another, make sure it's removed first
        # so it doesn't get removed again by set_content.
        for panel in self.panels:
            panel.clear_content()

        for panel, widget in zip(self.panels, content):
            panel.set_content(widget)

        self.pending_position = flex[0] / sum(flex)

    def get_direction(self):
        return {
            Orientation.Vertical: Direction.VERTICAL,
            Orientation.Horizontal: Direction.HORIZONTAL,
        }[self.native.Orientation]

    def set_direction(self, value):
        position = self.get_position()

        self.native.Orientation = {
            Direction.VERTICAL: Orientation.Vertical,
            Direction.HORIZONTAL: Orientation.Horizontal,
        }[value]

        self.set_position(position)

    def get_position(self):
        return self.native.SplitterDistance / self.get_max_position()

    def set_position(self, position):
        self.native.SplitterDistance = round(position * self.get_max_position())

    def get_max_position(self):
        return (
            self.native.Width
            if self.get_direction() == Direction.VERTICAL
            else self.native.Height
        )

    def resize_content(self, **kwargs):
        for panel in self.panels:
            size = panel.native_parent.ClientSize
            panel.resize_content(size.Width, size.Height, **kwargs)
