from rubicon.objc import NSPoint

from toga_cocoa.libs import NSEvent, NSEventType, NSSlider

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

    async def press(self):
        await self.mouse_event(NSEventType.LeftMouseDown)

    async def release(self):
        await self.mouse_event(NSEventType.LeftMouseUp)

    async def mouse_event(self, event_type):
        await self.post_event(
            NSEvent.mouseEventWithType(
                event_type,
                location=self.native.convertPoint(
                    NSPoint(self.width / 2, self.height / 2), toView=None
                ),
                modifierFlags=0,
                timestamp=0,
                windowNumber=self.native.window.windowNumber,
                context=None,
                eventNumber=0,
                clickCount=1,
                pressure=1.0 if event_type == NSEventType.LeftMouseDown else 0.0,
            ),
        )
