from travertino.size import at_least

from ..libs.android import R__attr, R__style
from ..libs.android.view import View__MeasureSpec
from ..libs.android.widget import SeekBar, SeekBar__OnSeekBarChangeListener
from .base import Widget


class TogaOnSeekBarChangeListener(SeekBar__OnSeekBarChangeListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onProgressChanged(self, _view, _progress, _from_user):
        self.impl.interface._sync_value()

    # Add two unused methods so that the Java interface is completely implemented.
    def onStartTrackingTouch(self, native_seekbar):
        pass

    def onStopTrackingTouch(self, native_seekbar):
        pass


# Since Android's SeekBar is always discrete,
# use a high number of steps for a "continuous" slider.
DEFAULT_NUMBER_OF_TICKS = 10000

TICK_DRAWABLE = None


class Slider(Widget):
    def create(self):
        self.native = SeekBar(self._native_activity)
        self.native.setMax(DEFAULT_NUMBER_OF_TICKS)
        self.native.setOnSeekBarChangeListener(TogaOnSeekBarChangeListener(self))

    def get_value(self):
        actual_value = self.native.getProgress()
        actual_max = self.native.getMax()
        minimum, maximum = self.interface.range
        span = maximum - minimum
        return actual_value / actual_max * span + minimum

    def set_value(self, value):
        minimum, maximum = self.interface.range
        span = maximum - minimum
        actual_max = self.native.getMax()
        self.native.setProgress(round((value - minimum) / span * actual_max))

    def set_range(self, range):
        pass

    def set_tick_count(self, tick_count):
        if tick_count is None:
            self.native.setTickMark(None)
            self.native.setMax(DEFAULT_NUMBER_OF_TICKS)
        else:
            if TICK_DRAWABLE is None:
                self._load_tick_drawable()
            self.native.setTickMark(TICK_DRAWABLE)
            self.native.setMax(tick_count - 1)

    def _load_tick_drawable(self):
        global TICK_DRAWABLE
        attrs = self._native_activity.obtainStyledAttributes(
            R__style.Widget_Material_SeekBar_Discrete, [R__attr.tickMark]
        )
        TICK_DRAWABLE = attrs.getDrawable(0)
        attrs.recycle()

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
