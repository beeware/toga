from PySide6.QtWidgets import QSlider

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = QSlider

    @property
    def position(self):
        return (self.native.value() - self._min) / (self._max - self._min)

    async def change(self, position):
        self.native.setValue(self._min + round(position * (self._max - self._min)))

    @property
    def tick_count(self):
        tick_position = self.native.tickPosition()
        match tick_position:
            case QSlider.TickPosition.NoTicks:
                return None
            case _:
                # anything else
                return (self._max + 1 - self._min) / self.native.tickInterval()

    @property
    def _min(self):
        return self.native.minimum()

    @property
    def _max(self):
        return self.native.maximum()

    async def press(self):
        self.native.sliderPressed.emit()

    async def release(self):
        self.native.sliderReleased.emit()
