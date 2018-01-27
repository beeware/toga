from rubicon.objc import *

from toga_iOS.color import native_color
from toga_iOS.libs import UIView, UIColor

from .base import Widget


class TogaView(UIView):
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

    def set_background_color(self, value):
        if value is None:
            self.native.backgroundColor = UIColor.whiteColor
        else:
            self.native.backgroundColor = native_color(value)
