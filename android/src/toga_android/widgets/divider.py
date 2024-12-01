from android.graphics import Color
from android.view import View
from android.widget import LinearLayout
from travertino.size import at_least

from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = View(self._native_activity)

        # Background color needs to be set or else divider will not be visible.
        self.native.setBackgroundColor(Color.LTGRAY)

        self._direction = self.interface.HORIZONTAL

    def set_background_color(self, value):
        # Do nothing, since background color of Divider shouldn't be changed.
        pass

    def get_direction(self):
        return self._direction

    def set_direction(self, value):
        self._direction = value

        if value == self.interface.VERTICAL:
            # Set the height for a vertical divider
            params = LinearLayout.LayoutParams(1, self.interface._MIN_HEIGHT)
        else:
            # Set the width for a horizontal divider
            params = LinearLayout.LayoutParams(self.interface._MIN_WIDTH, 1)

        self.native.setLayoutParams(params)

    def rehint(self):
        if self.get_direction() == self.interface.VERTICAL:
            self.interface.intrinsic.width = 1
            self.interface.intrinsic.height = at_least(self.native.getHeight())
        else:
            self.interface.intrinsic.width = at_least(self.native.getWidth())
            self.interface.intrinsic.height = 1
