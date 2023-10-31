from android.os import Build, SystemClock
from android.view import MotionEvent
from java import jclass

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = jclass("android.widget.SeekBar")

    @property
    def position(self):
        return (self.native.getProgress() - self._min) / (self._max - self._min)

    async def change(self, position):
        self.native.setProgress(self._min + round(position * (self._max - self._min)))

    @property
    def tick_count(self):
        if self.native.getTickMark():
            return self._max - self._min + 1
        else:
            return None

    @property
    def _min(self):
        return 0 if (Build.VERSION.SDK_INT < 26) else self.native.getMin()

    @property
    def _max(self):
        return self.native.getMax()

    async def press(self):
        self.native.onTouchEvent(self.motion_event(MotionEvent.ACTION_DOWN))

    async def release(self):
        self.native.onTouchEvent(self.motion_event(MotionEvent.ACTION_UP))

    def motion_event(self, action):
        time = SystemClock.uptimeMillis()
        return MotionEvent.obtain(
            time,  # downTime
            time,  # eventTime
            action,
            self.width / 2,
            self.height / 2,
            0,  # metaState
        )
