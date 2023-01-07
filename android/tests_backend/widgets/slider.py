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
    def tick_count(self):
        # The Android backend does not currently display tick marks, so assume that it's
        # in continuous mode if the range is very large.
        range = self._max - self._min + 1
        return range if range < 10000 else None

    @property
    def _min(self):
        return 0 if (Build.VERSION.SDK_INT < 26) else self.native.getMin()

    @property
    def _max(self):
        return self.native.getMax()
