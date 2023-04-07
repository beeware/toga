from travertino.size import at_least

import toga
from toga_winforms.libs import WinForms

from .base import Widget

# Implementation notes
# ====================
#
# The native widget represents values as integers, so the IntSliderImpl base class is
# used to convert between integers and floats.


# "None" is a reserved word in Python, so we can't write WinForms.TickStyle.None.
NONE_TICK_STYLE = getattr(WinForms.TickStyle, "None")
BOTTOM_RIGHT_TICK_STYLE = WinForms.TickStyle.BottomRight


class Slider(Widget, toga.widgets.slider.IntSliderImpl):
    def create(self):
        self.native = WinForms.TrackBar()
        self.native.AutoSize = False

        # Unlike Scroll, ValueChanged also fires when the value is changed
        # programmatically, such as via the testbed probe.
        self.native.ValueChanged += lambda sender, event: self.on_change()
        self.native.MouseDown += lambda sender, event: self.interface.on_press(None)
        self.native.MouseUp += lambda sender, event: self.interface.on_release(None)

    def get_int_value(self):
        return self.native.Value

    def set_int_value(self, value):
        self.native.Value = value

    def get_int_max(self):
        return self.native.Maximum

    def set_int_max(self, max):
        self.native.Maximum = max

    def set_ticks_visible(self, visible):
        self.native.TickStyle = BOTTOM_RIGHT_TICK_STYLE if visible else NONE_TICK_STYLE

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
