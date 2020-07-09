from travertino.size import at_least

from toga_cocoa.libs import SEL, NSSlider, objc_method

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

        self.set_tick_count(self.interface.tick_count)

        self.add_constraints()

    def set_tick_count(self, tick_count):
        if tick_count is None:
            self.native.allowsTickMarkValuesOnly = False
        else:
            self.native.allowsTickMarkValuesOnly = True
            self.native.numberOfTickMarks = tick_count

    def get_value(self):
        return self.native.floatValue

    def set_value(self, value):
        self.native.doubleValue = value

    def set_range(self, range):
        self.native.minValue = self.interface.range[0]
        self.native.maxValue = self.interface.range[1]

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.height = content_size.height
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)

    def set_on_slide(self, handler):
        pass
