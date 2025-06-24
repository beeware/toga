from decimal import ROUND_UP

from android import R
from android.view import View
from android.widget import SeekBar
from java import dynamic_proxy

from toga.widgets.slider import IntSliderImpl
from toga_android.widgets.base import ContainedWidget

# Implementation notes
# ====================
#
# The native widget represents values as integers, so the IntSliderImpl base class is
# used to convert between integers and floats.


class TogaOnSeekBarChangeListener(dynamic_proxy(SeekBar.OnSeekBarChangeListener)):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onProgressChanged(self, _view, _progress, _from_user):
        self.impl.on_change()

    def onStartTrackingTouch(self, native_seekbar):
        self.impl.interface.on_press()

    def onStopTrackingTouch(self, native_seekbar):
        self.impl.interface.on_release()


class Slider(ContainedWidget, IntSliderImpl):
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
            R.style.Widget_Material_SeekBar_Discrete, [R.attr.tickMark]
        )
        Slider.TICK_DRAWABLE = attrs.getDrawable(0)
        attrs.recycle()

    def rehint(self):
        self.native.measure(View.MeasureSpec.UNSPECIFIED, View.MeasureSpec.UNSPECIFIED)
        self.interface.intrinsic.height = self.scale_out(
            self.native.getMeasuredHeight(), ROUND_UP
        )
