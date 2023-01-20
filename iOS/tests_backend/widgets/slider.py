from toga_iOS.libs import UISlider

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = UISlider

    @property
    def position(self):
        return (self.native.value - self._min) / (self._max - self._min)

    def change(self, position):
        self.native.value = self._min + round(position * (self._max - self._min))

    @property
    def _min(self):
        return self.native.minimumValue

    @property
    def _max(self):
        return self.native.maximumValue
