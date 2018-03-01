from toga_winforms.libs import WinForms, Size, Point
from toga_winforms.window import WinFormsViewport

from .base import Widget


class SplitPanel:
    def __init__(self, panel, interface):
        self.native = panel
        self.native.interface = interface
        self.native.interface._impl = interface._impl


class SplitContainer(Widget):

    def create(self):
        self.native = WinForms.SplitContainer()
        self.native.interface = self.interface
        self.native.Resize += self.on_resize
        self.native.SplitterMoved += self.on_resize
        self.ratio = None
        self.panel1 = SplitPanel(self.native.Panel1, self.interface)
        self.panel2 = SplitPanel(self.native.Panel2, self.interface)

    def add_content(self, position, widget):
        widget.viewport = WinFormsViewport(self.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget
        if position >= 2:
            raise ValueError('SplitContainer content must be a 2-tuple')

        if position == 0:
            self.native.Panel1.Controls.Add(widget.native)
            widget.viewport = WinFormsViewport(self.panel1.native)

        elif position == 1:
            self.native.Panel2.Controls.Add(widget.native)
            widget.viewport = WinFormsViewport(self.panel2.native)

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

    def on_resize(self, sender, args):
        if self.interface.content:
            # Re-layout the content
            for content in self.interface.content:
                content.refresh()

    @property
    def vertical_shift(self):
        vertical_shift = 0
        try:
            if self.interface.window:
                if self.interface.window.content == self.interface:
                    vertical_shift = self.interface.window._impl.toolbar_native.Height
            return vertical_shift
        except AttributeError:
            return vertical_shift

    def set_bounds(self, x, y, width, height):
        # Top level containers need to be shifted down to take the toolbar
        # into account
        self.native.Size = Size(width, height)
        self.native.Location = Point(x, y + self.vertical_shift)
