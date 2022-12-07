import System.Windows.Forms

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = System.Windows.Forms.TrackBar

    @property
    def position(self):
        return (self.native.Value - self._min) / (self._max - self._min)

    def change(self, position):
        self.native.Value = self._min + round(position * (self._max - self._min))

    @property
    def _min(self):
        return self.native.Minimum

    @property
    def _max(self):
        return self.native.Maximum
