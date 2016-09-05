from toga.interface import SplitContainer as SplitContainerInterface

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
        if self._interface.window._impl.isVisible:
            # print ("SPLIT CONTAINER LAYOUT CHILDREN", self._interface._content[0]._impl.frame.size.width, self._interface._content[1]._impl.frame.size.width)
            self._interface._update_child_layout()


class SplitContainer(SplitContainerInterface, WidgetMixin):
    def __init__(self, id=None, style=None, direction=SplitContainerInterface.VERTICAL):
        super().__init__(id=None, style=None, direction=direction)
        self.startup()

    def startup(self):
        self._impl = NSSplitView.alloc().init()
        self._impl.setVertical_(self.direction)

        self._delegate = TogaSplitViewDelegate.alloc().init()
        self._delegate._interface = self

        self._impl.setDelegate_(self._delegate)

        # Add the layout constraints
        self._add_constraints()

    def _add_content(self, widget):
        self._impl.addSubview_(widget._impl)

    def _update_child_layout(self):
        """Force a layout update on the widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        for i, content in enumerate(self._content):
            frame = content._impl.frame
            content._update_layout(
                left=frame.origin.x,
                top=frame.origin.y,
                width=frame.size.width,
                height=frame.size.height
            )
