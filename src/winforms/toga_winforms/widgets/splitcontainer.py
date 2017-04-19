from ..container import Container
from ..libs import *
from .base import Widget


class SplitContainer(Widget):
    def create(self):
        self.native = WinForms.SplitContainer()

        self.ratio = None
        self.containers = []

    def add_content(self, position, widget):
        if widget.native is None:
            container = Container()
            container.content = widget
        else:
            container = widget

        self.containers.append(container)

        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            panel = self.native.Panel1
        elif position == 1:
            panel = self.native.Panel2

        panel.Controls.Add(container.native)

    def set_direction(self, value):
        self.native.Orientation = WinForms.Orientation.Vertical if value else WinForms.Orientation.Horizontal
