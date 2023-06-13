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
        self.interface.on_scroll(None)

    @objc_method
    def refreshContent(self):
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

    def content_refreshed(self):
        width = self.native.frame.size.width
        height = self.native.frame.size.height

        if self.interface._content:
            if self.interface.horizontal:
                width = max(self.interface.content.layout.width, width)

            if self.interface.vertical:
                height = max(self.interface.content.layout.height, height)

        self.native.contentSize = NSMakeSize(width, height)

    def get_vertical(self):
        return self._allow_vertical

    def set_vertical(self, value):
        self._allow_vertical = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large its content is.
        if self.interface.content:
            self.interface.refresh()

    def get_horizontal(self):
        return self._allow_horizontal

    def set_horizontal(self, value):
        self._allow_horizontal = value
        # If the scroll container has content, we need to force a refresh
        # to let the scroll container know how large its content is.
        if self.interface.content:
            self.interface.refresh()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def get_max_vertical_position(self):
        return max(
            0,
            self.native.contentSize.height - self.native.frame.size.height,
        )

    def get_vertical_position(self):
        return self.native.contentOffset.y

    def set_vertical_position(self, vertical_position):
        if vertical_position < 0:
            vertical_position = 0
        else:
            max_value = self.get_max_vertical_position()
            if vertical_position > max_value:
                vertical_position = max_value

        self.native.setContentOffset(
            NSMakePoint(self.native.contentOffset.x, vertical_position), animated=True
        )

    def get_max_horizontal_position(self):
        return max(
            0,
            self.native.contentSize.width - self.native.frame.size.width,
        )

    def get_horizontal_position(self):
        return self.native.contentOffset.x

    def set_horizontal_position(self, horizontal_position):
        if horizontal_position < 0:
            horizontal_position = 0
        else:
            max_value = self.get_max_horizontal_position()
            if horizontal_position > max_value:
                horizontal_position = max_value

        self.native.setContentOffset(
            NSMakePoint(horizontal_position, self.native.contentOffset.y), animated=True
        )
