from travertino.size import at_least

import toga

from ..libs.android import R__attr, R__style
from ..libs.android.view import View__MeasureSpec
from ..libs.android.widget import SeekBar, SeekBar__OnSeekBarChangeListener
from .base import Widget

# Implementation notes
# ====================
#
# The native widget represents values as integers, so the IntSliderImpl base class is
# used to convert between integers and floats.


class TogaOnSeekBarChangeListener(SeekBar__OnSeekBarChangeListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onProgressChanged(self, _view, _progress, _from_user):
        self.impl.on_change()

    def onStartTrackingTouch(self, native_seekbar):
        self.impl.interface.on_press(None)

    def onStopTrackingTouch(self, native_seekbar):
        self.impl.interface.on_release(None)


class Slider(Widget, toga.widgets.slider.IntSliderImpl):
    focusable = False
    TICK_DRAWABLE = None

    def create(self):
        self.native = SeekBar(self._native_activity)
        self.native.setOnSeekBarChangeListener(TogaOnSeekBarChangeListener(self))

    def get_int_value(self):
        return self.native.getProgress()

    def set_int_value(self, value):
        self.native.setProgress(value)

    def get_int_max(self):
        return self.native.getMax()

    def set_int_max(self, max):
        self.native.setMax(max)

    def set_ticks_visible(self, visible):
        if visible:
            if Slider.TICK_DRAWABLE is None:
                self._load_tick_drawable()
            self.native.setTickMark(Slider.TICK_DRAWABLE)
        else:
            self.native.setTickMark(None)

    def _load_tick_drawable(self):
        attrs = self._native_activity.obtainStyledAttributes(
            R__style.Widget_Material_SeekBar_Discrete, [R__attr.tickMark]
        )
        Slider.TICK_DRAWABLE = attrs.getDrawable(0)
        attrs.recycle()

    def rehint(self):
        self.native.measure(
            View__MeasureSpec.UNSPECIFIED, View__MeasureSpec.UNSPECIFIED
        )
        self.interface.intrinsic.width = at_least(self.native.getMeasuredWidth())
        self.interface.intrinsic.height = self.native.getMeasuredHeight()
