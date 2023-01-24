from toga_cocoa.libs import NSSlider

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = NSSlider

    @property
    def position(self):
        return (self.native.doubleValue - self._min) / (self._max - self._min)

    def change(self, position):
        self.native.doubleValue = self._min + round(position * (self._max - self._min))

    @property
    def _min(self):
        return self.native.minValue

    @property
    def _max(self):
        return self.native.maxValue
