from rubicon.objc import objc_method, SEL

from toga.interface import Slider as SliderInterface

from .base import WidgetMixin
from ..libs import UISlider, CGSize, UIControlEventValueChanged


class TogaSlider(UISlider):
    @objc_method
    def onSlide_(self, obj) -> None:
        if self._interface.on_slide:
            self._interface.on_slide(self._interface)

class Slider(SliderInterface, WidgetMixin):
    def __init__(self, default=None, range=None, id=None, style=None, on_slide=None, enabled=True):
        super().__init__(id=id, style=style, default=default, range=range, on_slide=on_slide, enabled=enabled)
        self._create()

    def create(self):
        self._impl = TogaSlider.alloc().init()
        self._impl._interface = self

        self._impl.continuous = True
        self._impl.addTarget_action_forControlEvents_(self._impl, SEL('onSlide:'), UIControlEventValueChanged)

        # Add the layout constraints
        self._add_constraints()

    def _get_value(self):
        return self._impl.value

    def _set_value(self, value):
        self._impl.setValue_animated_(value, True)

    def _set_range(self, range):
        self._impl.minimumValue = range.min
        self._impl.maximumValue = range.max

    def _set_enabled(self, value):
        self._impl.enabled = value

    def rehint(self):
        fitting_size = self._impl.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.style.hint(
            height=fitting_size.height,
            min_width=fitting_size.width,
        )