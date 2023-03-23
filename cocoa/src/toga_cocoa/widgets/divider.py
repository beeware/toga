from travertino.size import at_least

from toga_cocoa.libs import NSBox, NSBoxType

from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = NSBox.alloc().init()
        self.native.boxType = NSBoxType.NSBoxSeparator.value

        # Add the layout constraints
        self.add_constraints()

        # Set the initial direction
        self._direction = self.interface.HORIZONTAL

    def rehint(self):
        content_size = self.native.intrinsicContentSize()

        if self._direction == self.interface.VERTICAL:
            self.interface.intrinsic.width = content_size.width
            self.interface.intrinsic.height = at_least(content_size.height)
        else:
            self.interface.intrinsic.width = at_least(content_size.width)
            self.interface.intrinsic.height = content_size.height

    def get_direction(self):
        return self._direction

    def set_direction(self, value):
        self._direction = value
