from System.Windows.Forms import TickStyle, TrackBar

from .base import SimpleProbe


class SliderProbe(SimpleProbe):
    native_class = TrackBar

    @property
    def position(self):
        return (self.native.Value - self._min) / (self._max - self._min)

    async def change(self, position):
        self.native.Value = self._min + round(position * (self._max - self._min))

    @property
    def tick_count(self):
        tick_style = self.native.TickStyle
        if tick_style == TickStyle.BottomRight:
            return self._max - self._min + 1
        elif tick_style == getattr(TickStyle, "None"):
            return None
        else:
            raise ValueError(f"unknown TickStyle {tick_style}")

    @property
    def _min(self):
        return self.native.Minimum

    @property
    def _max(self):
        return self.native.Maximum

    async def press(self):
        self.native.OnMouseDown(self.mouse_event())

    async def release(self):
        self.native.OnMouseUp(self.mouse_event())
