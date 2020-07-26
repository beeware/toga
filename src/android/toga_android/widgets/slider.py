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
        if self.impl.interface.on_slide:
            self.impl.interface.on_slide(widget=self.impl.interface)

    # Add two unused methods so that the Java interface is completely implemented.
    def onStartTrackingTouch(self, native_seekbar):
        pass

    def onStopTrackingTouch(self, native_seekbar):
        pass


# Since Android's SeekBar is always discrete, use a high degree of steps for a "continuous" slider.
_DEFAULT_STEPS = 10000


class Slider(Widget):
    _min = 0
    _max = 1
    _steps = 100  # current `max` value in Android SeekBar

    def create(self):
        self.native = SeekBar(self._native_activity)
        self._set_steps(_DEFAULT_STEPS)
        self.native.setOnSeekBarChangeListener(TogaOnSeekBarChangeListener(self))

    def get_value(self):
        return (self.native.getProgress() * (self._max - self._min) / self._steps) + self._min

    def set_value(self, value):
        self.native.setProgress(int((self._max - value - self._min) * self._steps))

    def set_range(self, range):
        self._min = range[0]
        self._max = range[1]

        # Ensure current value is within range
        current_value = self.get_value()
        if current_value < self._min or current_value > self._max:
            self.set_value(self._min)

    def set_tick_count(self, tick_count):
        if tick_count is None:
            self._set_steps(_DEFAULT_STEPS)
        else:
            self._set_steps(int(tick_count) - 1)

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()

    def set_on_slide(self, handler):
        # No special handling required
        pass

    def _set_steps(self, steps):
        self._steps = steps
        self.native.setMax(steps)
