from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga.constants import Direction
from toga_cocoa.container import Container
from toga_cocoa.libs import NSSplitView

from .base import Widget


class TogaSplitView(NSSplitView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def splitViewDidResizeSubviews_(self, notification) -> None:
        # If the split has moved, a resize of all the content panels is required.
        for container in self.impl.sub_containers:
            if container.content:
                container.content.interface.refresh()

        # Apply any pending split
        self.performSelector(
            SEL("applySplit"),
            withObject=None,
            afterDelay=0,
        )

    @objc_method
    def applySplit(self) -> None:
        if self.impl._split_proportion:
            if self.interface.direction == self.interface.VERTICAL:
                position = self.impl._split_proportion * self.frame.size.width
            else:
                position = self.impl._split_proportion * self.frame.size.height

            self.setPosition(position, ofDividerAtIndex=0)
            self.impl._split_proportion = None


class SplitContainer(Widget):
    def create(self):
        self.native = TogaSplitView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        self.sub_containers = [
            Container(on_refresh=self.content_refreshed),
            Container(on_refresh=self.content_refreshed),
        ]
        self.native.addSubview(self.sub_containers[0].native)
        self.native.addSubview(self.sub_containers[1].native)

        self._split_proportion = None

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        for container in self.sub_containers:
            if container.content:
                container.content.interface.refresh()

        # Apply any pending split
        self.native.performSelector(
            SEL("applySplit"),
            withObject=None,
            afterDelay=0,
        )

    def content_refreshed(self, container):
        container.min_width = container.content.interface.layout.min_width
        container.min_height = container.content.interface.layout.min_height

    def set_content(self, content, flex):
        # Clear any existing content
        for container in self.sub_containers:
            container.content = None

        for index, widget in enumerate(content):
            self.sub_containers[index].content = widget

        # We now know the initial positions of the split. However, we can't *set* the
        # because Cocoa requires a pixel position, and the widget isn't visible yet.
        # So - store the split; and when have a displayed widget, apply that proportion.
        self._split_proportion = flex[0] / sum(flex)

    def get_direction(self):
        return Direction.VERTICAL if self.native.isVertical() else Direction.HORIZONTAL

    def set_direction(self, value):
        self.native.vertical = value

    def rehint(self):
        # This is a SWAG (scientific wild-ass guess). There doesn't appear to be
        # an actual API to get the true size of the splitter. 10px seems enough.
        SPLITTER_WIDTH = 10
        if self.interface.direction == self.interface.HORIZONTAL:
            # When the splitter is horizontal, the splitcontainer must be
            # at least as wide as it's widest sub-container, and at least
            # as tall as the minimum height of all subcontainers, plus the
            # height of the splitter itself. Enforce a minimum size in both
            # axies
            min_width = self.interface._MIN_WIDTH
            min_height = 0
            for sub_container in self.sub_containers:
                min_width = max(min_width, sub_container.min_width)
                min_height += sub_container.min_height

            min_height = max(min_height, self.interface._MIN_HEIGHT) + SPLITTER_WIDTH
        else:
            # When the splitter is vertical, the splitcontainer must be
            # at least as tall as it's tallest sub-container, and at least
            # as wide as the minimum width of all subcontainers, plus the
            # width of the splitter itself.
            min_width = 0
            min_height = self.interface._MIN_HEIGHT
            for sub_container in self.sub_containers:
                min_width += sub_container.min_width
                min_height = max(min_height, sub_container.min_height)

            min_width = max(min_width, self.interface._MIN_WIDTH) + SPLITTER_WIDTH

        self.interface.intrinsic.width = at_least(min_width)
        self.interface.intrinsic.height = at_least(min_height)
