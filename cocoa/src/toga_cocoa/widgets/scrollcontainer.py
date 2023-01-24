from travertino.size import at_least

from toga_cocoa.libs import NSColor, NSMakeRect, NSNoBorder, NSScrollView
from toga_cocoa.window import CocoaViewport

from .base import Widget


class ScrollContainer(Widget):
    def create(self):
        self.native = NSScrollView.alloc().init()
        self.native.autohidesScrollers = True
        self.native.borderType = NSNoBorder
        self.native.backgroundColor = NSColor.windowBackgroundColor

        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.autoresizesSubviews = True

        # Add the layout constraints
        self.add_constraints()

    def set_content(self, widget):
        self.native.documentView = widget.native
        widget.viewport = CocoaViewport(self.native.documentView)

        for child in widget.interface.children:
            child._impl.container = widget

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # Restrict dimensions of content to dimensions of ScrollContainer
        # along any non-scrolling directions. Set dimensions of content
        # to its layout dimensions along the scrolling directions.

        if self.interface.horizontal:
            width = self.interface.content.layout.width

        if self.interface.vertical:
            height = self.interface.content.layout.height

        self.interface.content._impl.native.frame = NSMakeRect(0, 0, width, height)

    def set_vertical(self, value):
        self.native.hasVerticalScroller = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large it's content is.
        if self.interface.content:
            self.interface.refresh()

    def set_horizontal(self, value):
        self.native.hasHorizontalScroller = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large it's content is.
        if self.interface.content:
            self.interface.refresh()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)

    def set_on_scroll(self, on_scroll):
        self.interface.factory.not_implemented("ScrollContainer.set_on_scroll()")

    def get_vertical_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_vertical_position()"
        )
        return 0

    def set_vertical_position(self, vertical_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_vertical_position()"
        )

    def get_horizontal_position(self):
        self.interface.factory.not_implemented(
            "ScrollContainer.get_horizontal_position()"
        )
        return 0

    def set_horizontal_position(self, horizontal_position):
        self.interface.factory.not_implemented(
            "ScrollContainer.set_horizontal_position()"
        )
