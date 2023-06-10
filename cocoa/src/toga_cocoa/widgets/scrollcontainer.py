from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga_cocoa.libs import (
    NSColor,
    NSMakePoint,
    NSMakeRect,
    NSNoBorder,
    NSNotificationCenter,
    NSScrollView,
    NSScrollViewDidEndLiveScrollNotification,
    NSScrollViewDidLiveScrollNotification,
)
from toga_cocoa.window import CocoaViewport

from .base import Widget


class TogaScrollView(NSScrollView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def didScroll_(self, note) -> None:
        # print(
        #     f"SCROLL frame={self.impl.native.frame.size.width}x{self.impl.native.frame.size.height}"
        #     f" @ {self.impl.native.frame.origin.x}x{self.impl.native.frame.origin.y}, "
        #     f"doc={self.impl.native.documentView.frame.size.width}x{self.impl.native.documentView.frame.size.height}"
        #     f" @ {self.impl.native.documentView.frame.origin.x}x{self.impl.native.documentView.frame.origin.y}, "
        #     f"content={self.impl.native.contentView.frame.size.width}x{self.impl.native.contentView.frame.size.height}"
        #     f" @ {self.impl.native.contentView.frame.origin.x}x{self.impl.native.contentView.frame.origin.y}, "
        # )
        self.interface.on_scroll(None)


class ScrollContainer(Widget):
    def create(self):
        self.native = TogaScrollView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.autohidesScrollers = True
        self.native.borderType = NSNoBorder
        self.native.backgroundColor = NSColor.windowBackgroundColor

        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.autoresizesSubviews = True

        NSNotificationCenter.defaultCenter.addObserver(
            self.native,
            selector=SEL("didScroll:"),
            name=NSScrollViewDidLiveScrollNotification,
            object=self.native,
        )
        NSNotificationCenter.defaultCenter.addObserver(
            self.native,
            selector=SEL("didScroll:"),
            name=NSScrollViewDidEndLiveScrollNotification,
            object=self.native,
        )

        # Add the layout constraints
        self.add_constraints()

    def set_content(self, widget):
        if widget:
            self.native.documentView = widget._impl.native
            widget._impl.viewport = CocoaViewport(self.native.documentView)

            for child in widget.children:
                child._impl.container = widget._impl
        else:
            self.native.documentView = None

    def set_bounds(self, x, y, width, height):
        # print("SET BOUNDS", x, y, width, height)
        super().set_bounds(x, y, width, height)
        # Restrict dimensions of content to dimensions of ScrollContainer
        # along any non-scrolling directions. Set dimensions of content
        # to its layout dimensions along the scrolling directions.
        if self.interface.horizontal:
            width = self.interface.content.layout.width

        if self.interface.vertical:
            height = self.interface.content.layout.height

        self.native.documentView.frame = NSMakeRect(0, 0, width, height)

    def get_vertical(self):
        return self.native.hasVerticalScroller

    def set_vertical(self, value):
        self.native.hasVerticalScroller = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large it's content is.
        if self.interface.content:
            self.interface.refresh()

    def get_horizontal(self):
        return self.native.hasHorizontalScroller

    def set_horizontal(self, value):
        self.native.hasHorizontalScroller = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large it's content is.
        if self.interface.content:
            self.interface.refresh()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def get_max_vertical_position(self):
        return max(
            0,
            self.native.documentView.bounds.size.height
            - self.native.contentView.bounds.size.height,
        )

    def get_vertical_position(self):
        return self.native.contentView.bounds.origin.y

    def set_vertical_position(self, vertical_position):
        if vertical_position < 0:
            vertical_position = 0
        else:
            max_value = self.get_max_vertical_position()
            if vertical_position > max_value:
                vertical_position = max_value

        new_position = NSMakePoint(
            self.native.contentView.bounds.origin.x,
            vertical_position,
        )
        self.native.contentView.scrollToPoint(new_position)
        self.native.reflectScrolledClipView(self.native.contentView)
        self.interface.on_scroll(None)

    def get_max_horizontal_position(self):
        return max(
            0,
            self.native.documentView.bounds.size.width
            - self.native.contentView.bounds.size.width,
        )

    def get_horizontal_position(self):
        return self.native.contentView.bounds.origin.x

    def set_horizontal_position(self, horizontal_position):
        if horizontal_position < 0:
            horizontal_position = 0
        else:
            max_value = self.get_max_horizontal_position()
            if horizontal_position > max_value:
                horizontal_position = max_value

        new_position = NSMakePoint(
            horizontal_position,
            self.native.contentView.bounds.origin.y,
        )
        self.native.contentView.scrollToPoint(new_position)
        self.native.reflectScrolledClipView(self.native.contentView)
        self.interface.on_scroll(None)
