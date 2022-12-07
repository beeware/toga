from java import jclass

from android.os import Build

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = jclass("android.widget.SeekBar")

    @property
    def position(self):
        return (self.native.getProgress() - self._min) / (self._max - self._min)

    def change(self, position):
        self.native.setProgress(self._min + round(position * (self._max - self._min)))

    @property
    def _min(self):
        return 0 if (Build.VERSION.SDK_INT < 26) else self.native.getMin()

    @property
    def _max(self):
        return self.native.getMax()
