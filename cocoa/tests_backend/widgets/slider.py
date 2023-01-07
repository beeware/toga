from toga_cocoa.libs import NSSlider

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = NSSlider

    @property
    def position(self):
        return (self.native.doubleValue - self._min) / (self._max - self._min)

    def change(self, position):
        self.native.doubleValue = self._min + (position * (self._max - self._min))
        self.native.performClick(None)

    @property
    def tick_count(self):
        if self.native.allowsTickMarkValuesOnly:
            return self.native.numberOfTickMarks
        else:
            assert self.native.numberOfTickMarks == 0
            return None

    @property
    def _min(self):
        return self.native.minValue

    @property
    def _max(self):
        return self.native.maxValue
