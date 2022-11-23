import System.Windows.Forms

from .probe_base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = System.Windows.Forms.TrackBar

    @property
    def position(self):
        min, max = self._range
        return (self.native.Value - min) / (max - min)

    def change(self, position):
        min, max = self._range
        self.native.Value = min + round(position * (max - min))

    @property
    def _range(self):
        return self.native.Minimum, self.native.Maximum
