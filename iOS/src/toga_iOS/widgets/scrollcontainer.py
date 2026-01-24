from rubicon.objc import (
    SEL,
    CGRectMake,
    NSMakePoint,
    NSMakeSize,
    objc_method,
    objc_property,
)
from travertino.size import at_least

from toga_iOS.container import Container
from toga_iOS.libs import (
    SUPPORTS_LIQUID_GLASS,
    UIScrollView,
    UIScrollViewContentInsetAdjustmentBehavior,
)
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
        # the size of the document content (assuming there is a document).
        # We can't reliably trigger the "no content" case in testbed, because it's
        # dependent on specific event timing.
        if self.interface._content:  # pragma: no branch
            self.interface._content.refresh()

    @objc_method
    def safeAreaInsetsDidChange(self) -> None:
        insets = self.safeAreaInsets

        self.contentInset.top = 0
        self.contentInset.bottom = 0
        self.contentInset.left = 0
        self.contentInset.right = 0

        if self.interface.vertical:
            self.contentInset.top = 0 if self.impl.bleed_top else insets.top
            self.contentInset.bottom = insets.bottom
        if self.interface.horizontal:
            self.contentInset.left = insets.left
            self.contentInset.right = insets.right


class ScrollContainer(Widget):
    def create(self):
        self.native = TogaScrollView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native
        self.native.contentInsetAdjustmentBehavior = (
            UIScrollViewContentInsetAdjustmentBehavior.Never
        )

        # UIScrollView doesn't have a native ability to disable a scrolling direction;
        # it's handled by controlling the scrollable area.
        self._allow_horizontal = True
        self._allow_vertical = True

        self.bleed_top = False

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

        self.bleed_top = (
            SUPPORTS_LIQUID_GLASS
            and y == -self.container.top_inset
            and self.interface.window
            and self.interface.window.bleed_top
            and self.interface.window._impl.container == self.container
        )

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

        # Update the document container frame to match the content size so that
        # buttons outside the original scroll view frame can receive touch events.
        # Without this, hit testing fails for views outside the original container
        # bounds
        self.document_container.native.frame = CGRectMake(0, 0, width, height)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def get_vertical(self):
        return self._allow_vertical

    def set_vertical(self, value):
        self._allow_vertical = value
        self.native.alwaysBounceVertical = value
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
        self.native.alwaysBounceHorizontally = value
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
