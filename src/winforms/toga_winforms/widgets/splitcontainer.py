from toga_winforms.libs import WinForms
from toga_winforms.window import WinFormsViewport

from .base import Widget


class SplitContainer(Widget):
    def create(self):
        self.native = WinForms.SplitContainer()
        self.native.interface = self.interface
        self.native.Resize += self.winforms_resize
        self.native.SplitterMoved += self.winforms_resize
        self.ratio = None

    def add_content(self, position, widget, flex):
        # TODO: Add flex option to the implementation
        widget.frame = self

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            self.native.Panel1.Controls.Add(widget.native)
            widget.viewport = WinFormsViewport(self.native.Panel1, self)

        elif position == 1:
            self.native.Panel2.Controls.Add(widget.native)
            widget.viewport = WinFormsViewport(self.native.Panel2, self)

            # Turn all the weights into a fraction of 1.0
            total = sum(self.interface._weight)
            self.interface._weight = [weight/total for weight in self.interface._weight]

            # Set the position of splitter depending on the weight of splits.
            total_distance = (
                self.native.Width
                if self.interface.direction == self.interface.VERTICAL
                else self.native.Height
            )
            self.native.SplitterDistance = int(
                self.interface._weight[0] * total_distance
            )

    def set_app(self, app):
        if self.interface.content:
            for content in self.interface.content:
                content.app = self.interface.app

    def set_window(self, window):
        if self.interface.content:
            for content in self.interface.content:
                content.window = self.interface.window

    def set_direction(self, value):
        self.native.Orientation = WinForms.Orientation.Vertical if value \
            else WinForms.Orientation.Horizontal

    def winforms_resize(self, sender, args):
        if self.interface.content:
            # Re-layout the content
            for content in self.interface.content:
                content.refresh()
