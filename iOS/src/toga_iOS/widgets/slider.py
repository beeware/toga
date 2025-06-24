from rubicon.objc import SEL, CGSize, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.libs import (
    UIControlEventTouchCancel,
    UIControlEventTouchDown,
    UIControlEventTouchUpInside,
    UIControlEventTouchUpOutside,
    UIControlEventValueChanged,
    UISlider,
)
from toga_iOS.widgets.base import Widget

# Implementation notes
# ====================
#
# UISlider is based on 32-bit floats, so we need to cache the value to allow
# round-tripping. We also need to cache the range, otherwise setting the max to 0.1, and
# then setting the value to 0.1, would fail with "0.1 is not in range 0.0 -
# 9.999999747378752e-02".
#
# UISlider does not support discrete mode. We simulate it by rounding the reported value
# to the closest tick, and resetting the thumb to that position after it's released.
# Ticks are not currently visible.


class TogaSlider(UISlider):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onSlide_(self, obj) -> None:
        self.impl.value = self.interface._round_value(self.value)
        self.interface.on_change()

    @objc_method
    def onPress_(self, obj) -> None:
        self.interface.on_press()

    @objc_method
    def onRelease_(self, obj) -> None:
        self.impl.set_value(self.impl.value)
        self.interface.on_release()


class Slider(Widget):
    def create(self):
        self.native = TogaSlider.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        # Dummy values used during initialization.
        self.value = 0
        self.min_value = 0
        self.max_value = 1
        self.tick_count = None

        self.native.addTarget(
            self.native,
            action=SEL("onSlide:"),
            forControlEvents=UIControlEventValueChanged,
        )
        self.native.addTarget(
            self.native,
            action=SEL("onPress:"),
            forControlEvents=UIControlEventTouchDown,
        )
        self.native.addTarget(
            self.native,
            action=SEL("onRelease:"),
            forControlEvents=UIControlEventTouchUpInside
            | UIControlEventTouchUpOutside
            | UIControlEventTouchCancel,
        )

        # Add the layout constraints
        self.add_constraints()

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        self.native.setValue(value, animated=True)

    def get_min(self):
        # Use the shadow copy, not the native value, to ensure round tripping.
        # See implementation notes for details.
        return self.min_value

    def set_min(self, value):
        self.min_value = value
        self.native.minimumValue = value

    def get_max(self):
        # Use the shadow copy, not the native value, to ensure round tripping.
        # See implementation notes for details.
        return self.max_value

    def set_max(self, value):
        self.max_value = value
        self.native.maximumValue = value

    def get_tick_count(self):
        return self.tick_count

    def set_tick_count(self, tick_count):
        self.tick_count = tick_count

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height
