from toga.interface import SplitContainer as SplitContainerInterface

from ..container import Container
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
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, direction=SplitContainerInterface.VERTICAL):
        super().__init__(id=None, style=style, direction=direction)
        self._create()

    def create(self):
        self._impl = NSSplitView.alloc().init()

        self._delegate = TogaSplitViewDelegate.alloc().init()
        self._delegate._interface = self

        self._impl.delegate = self._delegate

        # Add the layout constraints
        self._add_constraints()

    def _add_content(self, position, container):
        # Turn the autoresizing mask on the container widget
        # into constraints. This makes the container fill the
        # available space inside the SplitContainer.
        container._impl.translatesAutoresizingMaskIntoConstraints = True

        self._impl.addSubview(container._impl)

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
        self._impl.setVertical(value)

    def rehint(self):
        if self.content:
            if self.direction == SplitContainerInterface.VERTICAL:
                self.style.hint(
                    min_height=100,
                    min_width=100 * len(self.content)
                )
            else:
                self.style.hint(
                    min_height=100 * len(self.content),
                    min_width=100
                )
