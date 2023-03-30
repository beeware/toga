from rubicon.objc import SEL, CGSize, objc_method, objc_property
from travertino.size import at_least

import toga
from toga_iOS.libs import (
    UIControlEventTouchCancel,
    UIControlEventTouchDown,
    UIControlEventTouchUpInside,
    UIControlEventTouchUpOutside,
    UIControlEventValueChanged,
    UISlider,
)
from toga_iOS.widgets.base import Widget


class TogaSlider(UISlider):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onSlide_(self, obj) -> None:
        self.impl.on_change()

    @objc_method
    def onPress_(self, obj) -> None:
        self.impl.on_press()

    @objc_method
    def onRelease_(self, obj) -> None:
        self.impl.on_release()


class Slider(Widget, toga.widgets.slider.ContinuousSliderImpl):
    def create(self):
        self.native = TogaSlider.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        for method, events in [
            ("onSlide", UIControlEventValueChanged),
            ("onPress", UIControlEventTouchDown),
            (
                "onRelease",
                UIControlEventTouchUpInside
                | UIControlEventTouchUpOutside
                | UIControlEventTouchCancel,
            ),
        ]:
            self.native.addTarget(
                self.native, action=SEL(f"{method}:"), forControlEvents=events
            )

        # Add the layout constraints
        self.add_constraints()

    def get_continuous_value(self):
        return self.native.value

    def set_continuous_value(self, value):
        self.native.value = value

    def get_range(self):
        return self.range

    def set_range(self, range):
        self.native.minimumValue = range[0]
        self.native.maximumValue = range[1]

        # UISlider is based on 32-bit floats, so we need to cache the range. Otherwise,
        # for example, setting the max to 0.1, and then setting the value to the same
        # number, would fail with "0.1 is not in range 0.0 - 9.999999747378752e-02".
        self.range = range

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize_(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height
