from rubicon.objc import objc_method, SEL

from .base import Widget
from ..libs import *
from ..utils import process_callback


class TogaSlider(NSSlider):
    @objc_method
    def onSlide_(self, obj) -> None:
        if self.interface.on_slide:
            process_callback(self.interface.on_slide(self.interface))


class Slider(Widget):
    def create(self):
        self.native = TogaSlider.alloc().init()
        self.native.interface = self.interface

        self.native.target = self.native
        self.native.action = SEL('onSlide:')

        self.add_constraints()

    def get_value(self):
        return self.native.floatValue

    def set_value(self, value):
        self.native.doubleValue = value

    def set_range(self, range):
        self.native.minValue = range[0]
        self.native.maxValue = range[1]

    def set_enabled(self, value):
        self.native.enabled = value

    def rehint(self):
        fitting_size = self.native.fittingSize()
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
