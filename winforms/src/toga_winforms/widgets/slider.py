from decimal import ROUND_UP

import System.Windows.Forms as WinForms

from toga.widgets.slider import IntSliderImpl

from ..libs.wrapper import WeakrefCallable
from .base import Widget

# Implementation notes
# ====================
#
# The native widget represents values as integers, so the IntSliderImpl base class is
# used to convert between integers and floats.


# "None" is a reserved word in Python, so we can't write WinForms.TickStyle.None.
NONE_TICK_STYLE = getattr(WinForms.TickStyle, "None")
BOTTOM_RIGHT_TICK_STYLE = WinForms.TickStyle.BottomRight


class Slider(Widget, IntSliderImpl):
    def create(self):
        IntSliderImpl.__init__(self)
        self.native = WinForms.TrackBar()
        self.native.AutoSize = False

        # Unlike Scroll, ValueChanged also fires when the value is changed
        # programmatically, such as via the testbed probe.
        self.native.ValueChanged += WeakrefCallable(self.winforms_value_chaned)
        self.native.MouseDown += WeakrefCallable(self.winforms_mouse_down)
        self.native.MouseUp += WeakrefCallable(self.winforms_mouse_up)

    def winforms_value_chaned(self, sender, event):
        self.on_change()

    def winforms_mouse_down(self, sender, event):
        self.interface.on_press()

    def winforms_mouse_up(self, sender, event):
        self.interface.on_release()

    def get_int_value(self):
        return self.native.Value

    def set_int_value(self, value):
        self.native.Value = value

    def get_int_max(self):
        return self.native.Maximum

    def set_int_max(self, value):
        self.native.Maximum = value

    def set_ticks_visible(self, visible):
        self.native.TickStyle = BOTTOM_RIGHT_TICK_STYLE if visible else NONE_TICK_STYLE

    def rehint(self):
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )
