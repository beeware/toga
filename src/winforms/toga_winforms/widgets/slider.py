from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


# This is a patch related to python: "None" is a saved word in python,
# which means we cannot use WinForms.TickStyle.None directly. Therefore, we use getattr
NONE_TICK_STYLE = getattr(WinForms.TickStyle, "None")

BOTTOM_RIGHT_TICK_STYLE = WinForms.TickStyle.BottomRight

DEFAULT_NUMBER_OF_TICKS = 100


class TogaSlider(WinForms.TrackBar):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.Scroll += self.on_slide

    def on_slide(self, sender, event):
        if self.interface.on_slide:
            self.interface.on_slide(self.interface)


class Slider(Widget):
    def create(self):
        self.native = TogaSlider(self.interface)
        self.set_enabled(self.interface._enabled)
        self.native.Minimum = 0
        self.set_number_of_ticks(self.interface.number_of_ticks)

    def get_value(self):
        actual_value = self.native.Value
        actual_number_of_ticks = self.native.Maximum
        minimum, maximum = self.interface.range
        span = maximum - minimum
        value = actual_value / actual_number_of_ticks * span + minimum
        return value

    def set_value(self, value):
        minimum, maximum = self.interface.range
        span = maximum - minimum
        actual_number_of_ticks = self.native.Maximum
        self.native.Value = (value - minimum) / span * actual_number_of_ticks

    def set_range(self, range):
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_number_of_ticks(self, number_of_ticks):
        if number_of_ticks is None:
            self.native.TickStyle = NONE_TICK_STYLE
            self.native.Maximum = DEFAULT_NUMBER_OF_TICKS
        else:
            self.native.TickStyle = BOTTOM_RIGHT_TICK_STYLE
            self.native.Maximum = number_of_ticks - 1

    def set_on_slide(self, handler):
        pass
