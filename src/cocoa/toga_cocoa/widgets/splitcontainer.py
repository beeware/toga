from toga_cocoa.libs import *
from toga_cocoa.window import CocoaViewport

from .base import Widget


class TogaSplitViewDelegate(NSObject):
    @objc_method
    def splitView_resizeSubviewsWithOldSize_(self, view, size: NSSize) -> None:
        if size.width and size.height:
            count = len(self._impl.containers)

            # Turn all the weights into a fraction of 1.0
            total = sum(self.interface._weight)
            self.interface._weight = [
                weight / total
                for weight in self.interface._weight
            ]

            # Set the splitter positions based on the new weight fractions.
            for i, weight in enumerate(self.interface._weight[:-1]):
                view.setPosition(size.width * self.interface._weight[i], ofDividerAtIndex=i)
        view.adjustSubviews()

    @objc_method
    def splitViewDidResizeSubviews_(self, notification) -> None:
        # If the window is actually visible, and the split has moved,
        # a resize of all the content panels is required.
        if self.interface.window and self.interface.window._impl.native.isVisible:
            # print("SPLIT CONTAINER LAYOUT CHILDREN", self.interface._impl.containers[0].native.frame.size.width, self.interface._impl.containers[1].native.frame.size.width)
            self.interface.refresh()
            self.interface._impl.on_resize()


class SplitContainer(Widget):
    """ Cocoa SplitContainer implementation

    Todo:
        * update the minimum width of the whole SplitContainer based on the content of its sub layouts.
    """
    def create(self):
        self.native = NSSplitView.alloc().init()

        self.delegate = TogaSplitViewDelegate.alloc().init()
        self.delegate.interface = self.interface
        self.delegate._impl = self
        self.native.delegate = self.delegate

        # Add the layout constraints
        self.add_constraints()

    def add_content(self, position, widget):
        widget.viewport = CocoaViewport(widget.native)

        # Turn the autoresizing mask on the widget into constraints.
        # This makes the widget fill the available space inside the
        # SplitContainer.
        # FIXME Use Constrains to enforce min width and height of the widgets otherwise width of 0 is possible.
        widget.native.translatesAutoresizingMaskIntoConstraints = True
        self.native.addSubview(widget.native)

    def set_direction(self, value):
        self.native.vertical = value

    def on_resize(self):
        pass
