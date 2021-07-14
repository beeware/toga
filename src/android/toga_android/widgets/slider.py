from travertino.size import at_least

from ..libs.android.view import View__MeasureSpec
from ..libs.android.widget import SeekBar, SeekBar__OnSeekBarChangeListener
from .base import Widget


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
        if self.interface.tick_count is not None and self.interface.tick_count <= 1:
            return minimum
        toga_tick_count = self.interface.tick_count or DEFAULT_NUMBER_OF_TICKS
        android_slider_max = toga_tick_count - 1
        tick_factor = (maximum - minimum) / android_slider_max
        progress_scaled = self.native.getProgress() * tick_factor
        result = progress_scaled + minimum
        return result

    def set_value(self, value):
        minimum, maximum = self.interface.range
        if self.interface.tick_count is not None and self.interface.tick_count <= 1:
            android_progress = 0
        else:
            toga_tick_count = self.interface.tick_count or DEFAULT_NUMBER_OF_TICKS
            android_slider_max = toga_tick_count - 1
            tick_factor = (maximum - minimum) / android_slider_max
            android_progress = int((value - minimum) * tick_factor)
        self.native.setProgress(android_progress)

    def set_range(self, range):
        pass

    def set_tick_count(self, tick_count):
        # Since the Android slider slides from 0 to max inclusive, always subtract 1 from tick_count.
        if self.interface.tick_count is None:
            android_slider_max = DEFAULT_NUMBER_OF_TICKS - 1
        else:
            android_slider_max = int(self.interface.tick_count - 1)
        # Set the Android SeekBar max, clamping so it's non-negative.
        self.native.setMax(max(0, android_slider_max))

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
