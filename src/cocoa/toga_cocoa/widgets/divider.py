from travertino.size import at_least
from rubicon.objc import objc_method, SEL

from toga_cocoa.libs import NSBox, NSBoxSeparator

from .base import Widget


class TogaDivider(NSBox):
    pass


class Divider(Widget):
    def create(self):
        self.native = TogaDivider.alloc().init()
        self.native.interface = self.interface

        self.native.boxType = NSBoxSeparator

        # Add the layout constraints
        self.add_constraints()

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.width = at_least(content_size.width)
        self.interface.intrinsic.height = at_least(content_size.height)
