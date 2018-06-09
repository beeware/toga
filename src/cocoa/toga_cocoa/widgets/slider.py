from rubicon.objc import objc_method, SEL
from travertino.size import at_least

from toga_cocoa.libs import *

from .base import Widget


class TogaSlider(NSSlider):
    @objc_method
    def onSlide_(self, obj) -> None:
        if self.interface.on_slide:
            self.interface.on_slide(self.interface)


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
        self.native.doubleValue = self.interface.value

    def set_range(self, range):
        self.native.minValue = self.interface.range[0]
        self.native.maxValue = self.interface.range[1]

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.height = content_size.height
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)

    def set_on_slide(self, handler):
        pass
