from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_iOS.libs import UIView
from toga_iOS.widgets.base import Widget


class Box(Widget):
    def create(self):
        self.native = UIView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self._default_background_color = TRANSPARENT

        # Add the layout constraints
        self.add_constraints()

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
