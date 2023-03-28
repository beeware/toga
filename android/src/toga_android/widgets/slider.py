from travertino.size import at_least

import toga

from ..libs.android import R__attr, R__style
from ..libs.android.view import View__MeasureSpec
from ..libs.android.widget import SeekBar, SeekBar__OnSeekBarChangeListener
from .base import Widget


class TogaOnSeekBarChangeListener(SeekBar__OnSeekBarChangeListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onProgressChanged(self, _view, _progress, _from_user):
        self.impl.on_change()

    # Add two unused methods so that the Java interface is completely implemented.
    def onStartTrackingTouch(self, native_seekbar):
        pass

    def onStopTrackingTouch(self, native_seekbar):
        pass


TICK_DRAWABLE = None


class Slider(Widget, toga.widgets.slider.IntSliderImpl):
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
            if TICK_DRAWABLE is None:
                self._load_tick_drawable()
            self.native.setTickMark(TICK_DRAWABLE)
        else:
            self.native.setTickMark(None)

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

    def set_on_press(self, handler):
        self.interface.factory.not_implemented("Slider.set_on_press()")

    def set_on_release(self, handler):
        self.interface.factory.not_implemented("Slider.set_on_release()")
