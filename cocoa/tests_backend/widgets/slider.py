from rubicon.objc import NSPoint

from toga_cocoa.libs import NSEventType, NSSlider

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = NSSlider

    @property
    def position(self):
        return (self.native.doubleValue - self._min) / (self._max - self._min)

    def change(self, position):
        self.native.doubleValue = self._min + (position * (self._max - self._min))
        self.native.performClick(None)  # Setting the value doesn't trigger the action.

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

    async def press(self):
        await self.mouse_event(
            NSEventType.LeftMouseDown,
            self.native.convertPoint(
                NSPoint(self.width / 2, self.height / 2), toView=None
            ),
        )

    async def release(self):
        await self.mouse_event(
            NSEventType.LeftMouseUp,
            self.native.convertPoint(
                NSPoint(self.width / 2, self.height / 2), toView=None
            ),
        )

        # Synthesizing this event doesn't trigger the action, even though a real event
        # does (https://github.com/beeware/toga/pull/1708#issuecomment-1490964061).
        self.native.performClick(None)
