from toga_iOS.libs import UIStackView

from .base import SimpleProbe, UIControlEventValueChanged
from .properties import toga_color


class SwitchProbe(SimpleProbe):
    native_class = UIStackView

    def __init__(self, widget):
        super().__init__(widget)
        self.native_label = widget._impl.native_label
        self.native_switch = widget._impl.native_switch

    @property
    def enabled(self):
        return self.native_label.isEnabled() and self.native_switch.isEnabled()

    @property
    def text(self):
        return str(self.native_label.text)

    @property
    def color(self):
        return toga_color(self.native_label.textColor)

    @property
    def font(self):
        return self.native_label.font

    def assert_width(self, min_width, max_width):
        super().assert_width(min_width, max_width)

        # Also check the width of the two inner components
        label_width = self.native_label.frame.size.width
        switch_width = self.native_switch.frame.size.width

        # The switch should be ~51px wide.
        MAX_SWITCH_WIDTH = 60

        assert (
            (min_width - MAX_SWITCH_WIDTH)
            <= label_width
            <= (max_width - MAX_SWITCH_WIDTH)
        ), f"Label width ({label_width}) not in range ({min_width - MAX_SWITCH_WIDTH}, {max_width - MAX_SWITCH_WIDTH})"
        assert (
            0 <= switch_width <= MAX_SWITCH_WIDTH
        ), f"Switch width ({switch_width}) not in range (0-60)"

    def assert_height(self, min_height, max_height):
        super().assert_height(min_height, max_height)

        label_height = self.native_label.frame.size.height
        switch_height = self.native_switch.frame.size.height

        # label and switch height isn't affected by widget sizing
        assert (
            20 <= label_height <= 30
        ), f"Label height ({label_height}) not in range (20, 30)"
        assert (
            30 <= switch_height <= 40
        ), f"Switch height ({switch_height}) not in range (30, 40)"

    async def press(self):
        self.native_switch.sendActionsForControlEvents(UIControlEventValueChanged)
