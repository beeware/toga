from ..container import Container
from ..libs import *
from .base import Widget


class TogaSplitViewDelegate(NSObject):
    @objc_method
    def splitView_resizeSubviewsWithOldSize_(self, view, size: NSSize) -> None:
        view.adjustSubviews()

    @objc_method
    def splitViewDidResizeSubviews_(self, notification) -> None:
        # If the window is actually visible, and the split has moved,
        # a resize of all the content panels is required.
        if self.interface.interface.window and self.interface.interface.window._impl.native.isVisible:
            # print("SPLIT CONTAINER LAYOUT CHILDREN", self.interface._containers[0]._impl.frame.size.width, self._interface._containers[1]._impl.frame.size.width)
            self.interface._update_child_layout()
            self.interface.on_resize()


class SplitContainer(Widget):
    _CONTAINER_CLASS = Container

    def create(self):
        self.native = NSSplitView.alloc().init()

        self.delegate = TogaSplitViewDelegate.alloc().init()
        self.delegate.interface = self
        self.native.setDelegate_(self.delegate)

        # Add the layout constraints
        self.add_constraints()

    def add_content(self, position, container):
        # Turn the autoresizing mask on the container widget
        # into constraints. This makes the container fill the
        # available space inside the SplitContainer.
        container._impl.setTranslatesAutoresizingMaskIntoConstraints_(True)

        self.native.addSubview_(container._impl.native)

    def _update_child_layout(self):
        """Force a layout update on the widget.
        """
        if self.interface.content:
            for i, (container, content) in enumerate(zip(self.interface._containers, self.interface.content)):
                frame = container._impl.native.frame
                content._update_layout(
                    width=frame.size.width,
                    height=frame.size.height
                )

    def set_direction(self, value):
        self.native.setVertical_(value)

    def on_resize(self):
        pass