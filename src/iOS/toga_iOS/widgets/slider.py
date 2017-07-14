from rubicon.objc import objc_method, get_selector

from .base import Widget
from ..libs import UISlider, CGSize, UIControlEventValueChanged


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
        self.native.addTarget_action_forControlEvents_(self.native, get_selector('onSlide:'), UIControlEventValueChanged)

        # Add the layout constraints
        self.add_constraints()

    def get_value(self):
        return self.native.value

    def set_value(self, value):
        self.native.setValue_animated_(value, True)

    def set_range(self, range):
        self.native.minimumValue = range.min
        self.native.maximumValue = range.max

    def set_enabled(self, value):
        self.native.enabled = value

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )
