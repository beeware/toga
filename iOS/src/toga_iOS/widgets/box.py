from rubicon.objc import objc_property
from travertino.size import at_least

from toga_iOS.libs import UIView
from toga_iOS.widgets.base import Widget


class TogaView(UIView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)


class Box(Widget):
    def create(self):
        self.native = TogaView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Add the layout constraints
        self.add_constraints()

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
