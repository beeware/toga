from rubicon.objc import SEL, NSMakePoint, NSMakeSize, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.container import Container
from toga_iOS.libs import UIScrollView
from toga_iOS.widgets.base import Widget


class TogaScrollView(UIScrollView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def scrollViewDidScroll_(self, scrollView) -> None:
        self.interface.on_scroll()

    @objc_method
    def refreshContent(self):
        # Now that we have an updated size for the ScrollContainer, re-evaluate
        # the size of the document content (assuming there is a document)
        if self.interface._content:
            self.interface._content.refresh()


class ScrollContainer(Widget):
    def create(self):
        self.native = TogaScrollView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        # UIScrollView doesn't have a native ability to disable a scrolling direction;
        # it's handled by controlling the scrollable area.
        self._allow_horizontal = True
        self._allow_vertical = True

        self.document_container = Container(
            layout_native=self.native,
            on_refresh=self.content_refreshed,
        )
        self.native.addSubview(self.document_container.native)
        self.add_constraints()

    def set_content(self, widget):
        self.document_container.content = widget

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # Setting the bounds changes the constraints, but that doesn't mean
        # the constraints have been fully applied. Schedule a refresh to be done
        # as soon as possible in the future
        self.native.performSelector(
            SEL("refreshContent"), withObject=None, afterDelay=0
        )

    def content_refreshed(self, container):
        width = self.native.frame.size.width
        height = self.native.frame.size.height

        if self.interface.horizontal:
            width = max(self.interface.content.layout.width, width)

        if self.interface.vertical:
            height = max(self.interface.content.layout.height, height)

        self.native.contentSize = NSMakeSize(width, height)

    def set_background_color(self, value):
        self.set_background_color_simple(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def get_vertical(self):
        return self._allow_vertical

    def set_vertical(self, value):
        self._allow_vertical = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large its content is.
        if self.interface.content:
            self.interface.refresh()

        # Disabling scrolling implies a position reset; that's a scroll event.
        if not value:
            self.interface.on_scroll()

    def get_horizontal(self):
        return self._allow_horizontal

    def set_horizontal(self, value):
        self._allow_horizontal = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large its content is.
        if self.interface.content:
            self.interface.refresh()

        # Disabling scrolling implies a position reset; that's a scroll event.
        if not value:
            self.interface.on_scroll()

    def get_horizontal_position(self):
        if not self.get_horizontal():
            return 0
        return int(self.native.contentOffset.x)

    def get_max_vertical_position(self):
        return max(
            0,
            int(self.native.contentSize.height - self.native.frame.size.height),
        )

    def get_max_horizontal_position(self):
        return max(
            0,
            int(self.native.contentSize.width - self.native.frame.size.width),
        )

    def get_vertical_position(self):
        if not self.get_vertical():
            return 0
        return int(self.native.contentOffset.y)

    def set_position(self, horizontal_position, vertical_position):
        if (
            horizontal_position == self.get_horizontal_position()
            and vertical_position == self.get_vertical_position()
        ):
            # iOS doesn't generate a scroll event unless the position actually changes.
            # Treat all scroll position assignments as a change.
            self.interface.on_scroll()
        else:
            self.native.setContentOffset(
                NSMakePoint(horizontal_position, vertical_position), animated=True
            )
