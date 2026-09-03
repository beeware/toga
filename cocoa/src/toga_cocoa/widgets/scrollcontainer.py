import asyncio

from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga_cocoa.container import Container
from toga_cocoa.libs import (
    NSColor,
    NSMakePoint,
    NSMakeRect,
    NSNoBorder,
    NSNotificationCenter,
    NSPreferredScrollerStyleDidChangeNotification,
    NSScrollElasticityAllowed,
    NSScrollElasticityAutomatic,
    NSScrollElasticityNone,
    NSScrollView,
    NSScrollViewDidEndLiveScrollNotification,
    NSScrollViewDidLiveScrollNotification,
    NSSize,
)

from .base import Widget


class TogaScrollView(NSScrollView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def didScroll_(self, note) -> None:
        self.interface.on_scroll()

    @objc_method
    def refreshContent(self):
        # Now that we have an updated size for the ScrollContainer, re-evaluate
        # the size of the document content (assuming there is a document)
        if self.interface._content:
            self.interface._content.refresh()

    @objc_method
    def scrollerStyleChanged_(self, notification) -> None:
        # NSScrollView updates its scroller style from the system preference at runtime.
        # Wait until that update has completed before recomputing the content minimum.
        self.performSelector(SEL("refreshContent"), withObject=None, afterDelay=0)

    # This cannot be covered in CI because the function used to emit
    # a scrolling event is unreliable.
    @objc_method
    def wantsForwardedScrollEventsForAxis_(self, axis: int) -> bool:  # pragma: no cover
        return True


class ScrollContainer(Widget):
    def create(self):
        self.native = TogaScrollView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self.native.autohidesScrollers = True
        self.native.borderType = NSNoBorder
        self.native.backgroundColor = NSColor.windowBackgroundColor

        # The container for the document bases its layout on the
        # size of the content view. It can only exceed the size
        # of the contentView if scrolling is enabled in that axis.
        self.document_container = Container(
            layout_native=self.native.contentView,
            on_refresh=self.content_refreshed,
        )
        self.native.documentView = self.document_container.native

        NSNotificationCenter.defaultCenter.addObserver(
            self.native,
            selector=SEL("didScroll:"),
            name=NSScrollViewDidLiveScrollNotification,
            object=self.native,
        )
        NSNotificationCenter.defaultCenter.addObserver(
            self.native,
            selector=SEL("scrollerStyleChanged:"),
            name=NSPreferredScrollerStyleDidChangeNotification,
            object=None,
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
        # Set the document container's content to the new widget
        self.document_container.content = widget

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # Setting the bounds changes the constraints, but that doesn't mean
        # the constraints have been fully applied. Force realization of the
        # new layout, and then refresh the content.
        self.native.layoutSubtreeIfNeeded()
        self.native.refreshContent()

    def content_refreshed(self, container):
        width = self.native.frame.size.width
        height = self.native.frame.size.height

        # If scrolling is enabled in a given axis, the document container
        # has a minimum size equal to the layout width in that axis.
        # Otherwise, the document container has the same size as the
        # widget that holds the document being scrolled.
        if self.interface.horizontal:
            width = max(self.interface.content.layout.width, width)

        if self.interface.vertical:
            height = max(self.interface.content.layout.height, height)

        self.native.documentView.frame = NSMakeRect(0, 0, width, height)

        # Setting the document frame determines which non-overlay scrollers are
        # visible. Use the resulting viewport so a visible scroller doesn't create
        # overflow in the other axis.
        viewport_size = self.native.contentSize
        width = viewport_size.width
        height = viewport_size.height
        if self.interface.horizontal:
            width = max(self.interface.content.layout.width, width)
        if self.interface.vertical:
            height = max(self.interface.content.layout.height, height)
        self.native.documentView.frame = NSMakeRect(0, 0, width, height)

        previous_intrinsic_size = (
            self.interface.intrinsic.width,
            self.interface.intrinsic.height,
        )
        self.rehint()
        if previous_intrinsic_size != (
            self.interface.intrinsic.width,
            self.interface.intrinsic.height,
        ):
            asyncio.get_running_loop().call_soon_threadsafe(self.interface.refresh)

    def update_scroll_elasticity(self):
        # If both horizontal and vertical scrolling
        # is allowed, bounce horizontally only if
        # the content is actually scrollable (aka. overflows)
        # in that direction.  This mirrors the behavior
        # in Finder.
        if self.interface.horizontal:
            self.native.horizontalScrollElasticity = (
                NSScrollElasticityAllowed
                if not self.interface.vertical
                else NSScrollElasticityAutomatic
            )
        else:
            self.native.horizontalScrollElasticity = NSScrollElasticityNone
        self.native.verticalScrollElasticity = (
            NSScrollElasticityAllowed
            if self.interface.vertical
            else NSScrollElasticityNone
        )

    def get_vertical(self):
        return self.native.hasVerticalScroller

    def set_vertical(self, value):
        self.native.hasVerticalScroller = value
        # Disabling scrolling implies a position reset; that's a scroll event.
        if not value:
            self.interface.on_scroll()
        self.update_scroll_elasticity()

    def get_horizontal(self):
        return self.native.hasHorizontalScroller

    def set_horizontal(self, value):
        self.native.hasHorizontalScroller = value
        # Disabling scrolling implies a position reset; that's a scroll event.
        if not value:
            self.interface.on_scroll()
        self.update_scroll_elasticity()

    def rehint(self):
        min_width = self.interface._MIN_WIDTH
        min_height = self.interface._MIN_HEIGHT

        if self.interface.content:
            horizontal_scroller = self.native.horizontalScroller
            vertical_scroller = self.native.verticalScroller
            horizontal_scroller_class = (
                horizontal_scroller.objc_class
                if self.interface.horizontal and not horizontal_scroller.isHidden()
                else None
            )
            vertical_scroller_class = (
                vertical_scroller.objc_class
                if self.interface.vertical and not vertical_scroller.isHidden()
                else None
            )
            if horizontal_scroller_class:
                control_size = horizontal_scroller.controlSize
            elif vertical_scroller_class:
                control_size = vertical_scroller.controlSize
            else:
                control_size = 0
            frame_size = NSScrollView.frameSizeForContentSize(
                NSSize(
                    self.interface.content.layout.min_width,
                    self.interface.content.layout.min_height,
                ),
                horizontalScrollerClass=horizontal_scroller_class,
                verticalScrollerClass=vertical_scroller_class,
                borderType=self.native.borderType,
                controlSize=control_size,
                scrollerStyle=self.native.scrollerStyle,
            )

            if not self.interface.horizontal:
                min_width = max(min_width, frame_size.width)
            if not self.interface.vertical:
                min_height = max(min_height, frame_size.height)

        self.interface.intrinsic.width = at_least(min_width)
        self.interface.intrinsic.height = at_least(min_height)

    def get_max_vertical_position(self):
        return max(
            0,
            int(
                self.native.documentView.bounds.size.height
                - self.native.contentSize.height
            ),
        )

    def get_vertical_position(self):
        if not self.get_vertical():
            return 0
        return int(self.native.contentView.bounds.origin.y)

    def get_max_horizontal_position(self):
        return max(
            0,
            int(
                self.native.documentView.bounds.size.width
                - self.native.contentSize.width
            ),
        )

    def get_horizontal_position(self):
        if not self.get_horizontal():
            return 0
        return int(self.native.contentView.bounds.origin.x)

    def set_position(self, horizontal_position, vertical_position):
        new_position = NSMakePoint(horizontal_position, vertical_position)
        self.native.contentView.scrollToPoint(new_position)
        self.native.reflectScrolledClipView(self.native.contentView)
        self.interface.on_scroll()
