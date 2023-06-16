from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga.constants import Direction
from toga_cocoa.container import Container, MinimumContainer
from toga_cocoa.libs import NSSplitView

from .base import Widget


class TogaSplitView(NSSplitView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def splitViewDidResizeSubviews_(self, notification) -> None:
        # If the split has moved, a resize of all the content panels is required.
        for container in self.impl.sub_containers:
            container.content.interface.refresh()

        # If there's a pending split assignment, apply it.
        if self.impl._split_proportion:
            self.performSelector(
                SEL("applySplit"),
                withObject=None,
                afterDelay=0,
            )

    @objc_method
    def applySplit(self) -> None:
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

        self.sub_containers = [Container(), Container()]
        self.native.addSubview(self.sub_containers[0].native)
        self.native.addSubview(self.sub_containers[1].native)

        self._split_proportion = None

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        for container in self.sub_containers:
            container.content.interface.refresh()

        if self._split_proportion:
            self.native.performSelector(
                SEL("applySplit"),
                withObject=None,
                afterDelay=0,
            )

    def set_content(self, content, flex):
        # Clear any existing content
        for container in self.sub_containers:
            container.content = None

        for index, (widget, widget_flex) in enumerate(zip(content, flex)):
            # Compute the minimum layout for the content
            widget.interface.style.layout(widget.interface, MinimumContainer())
            min_width = widget.interface.layout.width
            min_height = widget.interface.layout.height

            # Create a container with that minimum size, and assign the widget as content
            self.sub_containers[index].min_width = min_width
            self.sub_containers[index].min_height = min_height

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
        min_width = 0
        min_height = 0
        for container in self.sub_containers:
            min_width += container.min_width
            min_height += container.min_height

        self.interface.intrinsic.width = at_least(
            max(self.interface._MIN_WIDTH, min_width)
        )
        self.interface.intrinsic.height = at_least(
            max(self.interface._MIN_HEIGHT, min_height)
        )
