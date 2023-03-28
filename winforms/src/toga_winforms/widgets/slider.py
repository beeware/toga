from travertino.size import at_least

import toga
from toga_winforms.libs import WinForms

from .base import Widget

# This is a patch related to python: "None" is a saved word in python,
# which means we cannot use WinForms.TickStyle.None directly. Therefore, we use getattr
NONE_TICK_STYLE = getattr(WinForms.TickStyle, "None")

BOTTOM_RIGHT_TICK_STYLE = WinForms.TickStyle.BottomRight


class Slider(Widget, toga.widgets.slider.IntSliderImpl):
    def create(self):
        self.native = WinForms.TrackBar()

        # Unlike Scroll, ValueChanged also fires when the value is changed
        # programmatically, such as via the testbed probe.
        self.native.ValueChanged += self.winforms_scroll
        self.native.MouseDown += self.winforms_mouse_down
        self.native.MouseUp += self.winforms_mouse_up

        self.set_enabled(self.interface._enabled)

    def winforms_scroll(self, sender, event):
        self.on_change()

    def winforms_mouse_down(self, sender, event):
        """Since picking and releasing the slider is also a change, calling the
        on_change method."""
        if self.container and self.interface.on_press:
            self.interface.on_press(self.interface)
        self.winforms_scroll(sender, event)

    def winforms_mouse_up(self, sender, event):
        """Since picking and releasing the slider is also a change, calling the
        on_change method."""
        self.winforms_scroll(sender, event)
        if self.container and self.interface.on_release:
            self.interface.on_release(self.interface)

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
