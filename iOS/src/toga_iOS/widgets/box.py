from rubicon.objc import objc_method, objc_property

from toga_iOS.colors import native_color
from toga_iOS.libs import UIColor, UIView
from toga_iOS.widgets.base import Widget


class TogaView(UIView):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

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
        self.native.interface = self.interface
        self.native.impl = self

        # Add the layout constraints
        self.add_constraints()

    def set_background_color(self, value):
        if value:
            self.native.backgroundColor = native_color(value)
        else:
            try:
                self.native.backgroundColor = UIColor.systemBackgroundColor()  # iOS 13+
            except AttributeError:
                self.native.backgroundColor = UIColor.whiteColor
