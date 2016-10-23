from toga.interface import SplitContainer as SplitContainerInterface

from ..container import TogaContainer
from ..libs import *
from .base import WidgetMixin


class TogaSplitViewDelegate(NSObject):
    @objc_method
    def splitView_resizeSubviewsWithOldSize_(self, view, size: NSSize) -> None:
        view.adjustSubviews()

    @objc_method
    def splitViewDidResizeSubviews_(self, notification) -> None:
        # If the window is actually visible, and the split has moved,
        # a resize of all the content panels is required.
        if self._interface.window and self._interface.window._impl.isVisible:
            # print("SPLIT CONTAINER LAYOUT CHILDREN", self._interface._containers[0]._impl.frame.size.width, self._interface._containers[1]._impl.frame.size.width)
            self._interface._update_child_layout()
            self._interface.on_resize()


class SplitContainer(SplitContainerInterface, WidgetMixin):
    def __init__(self, id=None, style=None, direction=SplitContainerInterface.VERTICAL):
        super().__init__(id=None, style=None, direction=direction)
        self._create()

    def create(self):
        self._impl = NSSplitView.alloc().init()

        self._delegate = TogaSplitViewDelegate.alloc().init()
        self._delegate._interface = self

        self._impl.setDelegate_(self._delegate)

        # Add the layout constraints
        self._add_constraints()

    def _add_content(self, position, container):
        self._impl.addSubview_(container._impl)

    def _update_child_layout(self):
        """Force a layout update on the widget.
        """
        if self.content:
            for i, (container, content) in enumerate(zip(self._containers, self.content)):
                frame = container._impl.frame
                content._update_layout(
                    width=frame.size.width,
                    height=frame.size.height
                )

    def _set_direction(self, value):
        self._impl.setVertical_(value)
