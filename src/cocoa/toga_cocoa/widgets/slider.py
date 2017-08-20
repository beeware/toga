from rubicon.objc import objc_method, SEL

from toga.interface import Slider as SliderInterface

from .base import WidgetMixin
from ..libs import *
from ..utils import process_callback


class TogaSlider(NSSlider):
    @objc_method
    def onSlide_(self, obj) -> None:
        if self._interface.on_slide:
            process_callback(self._interface.on_slide(self._interface))


class Slider(SliderInterface, WidgetMixin):
    def __init__(self, default=None, range=None, id=None, style=None, on_slide=None, enabled=True):
        super().__init__(id=id, style=style, default=default, range=range, on_slide=on_slide, enabled=enabled)
        self._create()
        self.rehint()

    def create(self):
        self._impl = TogaSlider.alloc().init()
        self._impl._interface = self

        self._impl.setTarget_(self._impl)
        self._impl.setAction_(SEL('onSlide:'))

        self._add_constraints()

    def _get_value(self):
        return self._impl.floatValue

    def _set_value(self, value):
        self._impl.setDoubleValue_(value)

    def _set_range(self, range):
        self._impl.setMinValue_(range.min)
        self._impl.setMaxValue_(range.max)

    def _set_enabled(self, value):
        self._impl.setEnabled_(value)

    def rehint(self):
        fitting_size = self._impl.fittingSize()
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
