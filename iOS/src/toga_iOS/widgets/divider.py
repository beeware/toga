from travertino.size import at_least

from toga_iOS.libs import UIColor
from toga_iOS.widgets.base import Widget

from .box import TogaView


class Divider(Widget):
    def create(self):
        self.native = TogaView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Background color needs to be set or else divider will not be visible.
        self.system_gray_color = UIColor.systemGrayColor()
        self.native.backgroundColor = self.system_gray_color

        # Add the layout constraints
        self.add_constraints()

        # Set the initial direction
        self._direction = self.interface.HORIZONTAL

    def set_background_color(self, value):
        # Do nothing, since background color of Divider shouldn't be changed.
        pass

    def rehint(self):
        content_size = self.native.intrinsicContentSize()

        if self._direction == self.interface.VERTICAL:
            self.interface.intrinsic.width = 1
            self.interface.intrinsic.height = at_least(content_size.height)
        else:
            self.interface.intrinsic.width = at_least(content_size.width)
            self.interface.intrinsic.height = 1

    def get_direction(self):
        return self._direction

    def set_direction(self, value):
        self._direction = value
