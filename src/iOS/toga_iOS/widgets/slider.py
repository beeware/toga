from rubicon.objc import SEL, CGSize, objc_method
from travertino.size import at_least

from toga_iOS.libs import UIControlEventValueChanged, UISlider
from toga_iOS.widgets.base import Widget


class TogaSlider(UISlider):
    @objc_method
    def onSlide_(self, obj) -> None:
        if self.interface.on_slide:
            self.interface.on_slide(self.interface)


class Slider(Widget):
    def create(self):
        self.native = TogaSlider.alloc().init()
        self.native.interface = self.interface

        self.native.continuous = True
        self.native.addTarget_action_forControlEvents_(self.native, SEL('onSlide:'), UIControlEventValueChanged)

        # Add the layout constraints
        self.add_constraints()

    def get_value(self):
        return self.native.value

    def set_value(self, value):
        self.native.setValue_animated_(value, True)

    def set_range(self, range):
        self.native.minimumValue = range[0]
        self.native.maximumValue = range[1]

    def set_tick_count(self, tick_count):
        self.interface.factory.not_implemented('Slider.tick_count()')

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height

    def set_on_slide(self, handler):
        # No special handling required
        pass
