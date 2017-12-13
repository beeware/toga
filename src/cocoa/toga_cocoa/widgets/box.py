from rubicon.objc import *

from toga_cocoa.widgets.base import Widget

from toga_cocoa.libs import NSView


class TogaView(NSView):
    @objc_method
    def isFlipped(self) -> bool:
        # Default Cocoa coordinate frame is around the wrong way.
        return True

    @objc_method
    def display(self) -> None:
        self.layer.setNeedsDisplay_(True)
        self.layer.displayIfNeeded()


class Box(Widget):
    def create(self):
        self.native = TogaView.alloc().init()

        # Add the layout constraints
        self.add_constraints()
