from travertino.size import at_least

from .base import Widget

from ..libs.android_widgets import (
    SeekBar,
    SeekBar__OnSeekBarChangeListener,
    View__MeasureSpec,
)


class TogaOnSeekBarChangeListener(SeekBar__OnSeekBarChangeListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onProgressChanged(self, _view, _progress, _from_user):
        if self.impl.interface.on_change:
            self.impl.interface.on_change(widget=self.impl.interface)

    # Add two unused methods so that the Java interface is completely implemented.
    def onStartTrackingTouch(self, native_seekbar):
        pass

    def onStopTrackingTouch(self, native_seekbar):
        pass


# Since Android's SeekBar is always discrete,
# use a high number of steps for a "continuous" slider.
DEFAULT_NUMBER_OF_TICKS = 10000


class Slider(Widget):
    def create(self):
        self.native = SeekBar(self._native_activity)
        self.native.setMax(DEFAULT_NUMBER_OF_TICKS)
        self.native.setOnSeekBarChangeListener(TogaOnSeekBarChangeListener(self))

    def get_value(self):
        minimum, maximum = self.interface.range
        n_steps = self.interface.tick_count
        if n_steps is None:
            n_steps = DEFAULT_NUMBER_OF_TICKS
        return (self.native.getProgress() * (maximum - minimum) / n_steps) + minimum

    def set_value(self, value):
        minimum, maximum = self.interface.range
        n_steps = self.interface.tick_count
        if n_steps is None:
            n_steps = DEFAULT_NUMBER_OF_TICKS
        self.native.setProgress(int((maximum - value - minimum) * n_steps))

    def set_range(self, range):
        pass

    def set_tick_count(self, tick_count):
        if tick_count is None:
            self.native.setMax(DEFAULT_NUMBER_OF_TICKS)
        else:
            self.native.setMax(int(tick_count) - 1)

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_on_change(self, handler):
        # No special handling required
        pass

    def set_on_press(self, handler):
        self.interface.factory.not_implemented("Slider.set_on_press()")

    def set_on_release(self, handler):
        self.interface.factory.not_implemented("Slider.set_on_release()")
