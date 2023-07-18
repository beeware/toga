from toga_iOS.libs import UISlider

from .base import SimpleProbe, UIControlEventTouchUpInside, UIControlEventValueChanged


class SliderProbe(SimpleProbe):
    native_class = UISlider

    @property
    def position(self):
        return (self.native.value - self._min) / (self._max - self._min)

    async def change(self, position):
        self.native.value = self._min + (position * (self._max - self._min))
        self.native.sendActionsForControlEvents(UIControlEventValueChanged)

    @property
    def tick_count(self):
        raise NotImplementedError()

    @property
    def _min(self):
        return self.native.minimumValue

    @property
    def _max(self):
        return self.native.maximumValue

    async def release(self):
        self.native.sendActionsForControlEvents(UIControlEventTouchUpInside)
