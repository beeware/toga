from __future__ import annotations

import asyncio
from datetime import datetime, time, timedelta

from .base import SimpleProbe


class TimeInputProbe(SimpleProbe):
    def __init__(self, widget):
        super().__init__(widget)
        self.widget = widget

        prev = widget.value
        try:
            widget.value = time(12, 34, 56)
            self.supports_seconds = widget.value and widget.value.second == 56
        except Exception:
            self.supports_seconds = False
        finally:
            widget.value = prev

    @property
    def value(self) -> time | None:
        return self.widget.value

    async def change(self, delta_minutes: int):
        if callable(getattr(self, "redraw", None)):
            await self.redraw(f"TimeInput change {delta_minutes:+d} min")

        cur = self.widget.value or self.widget.min or time(0, 0, 0)
        new_dt = datetime(2000, 1, 1, cur.hour, cur.minute, cur.second) + timedelta(
            minutes=int(delta_minutes)
        )
        t = time(new_dt.hour, new_dt.minute, new_dt.second)
        tmin, tmax = self.widget.min, self.widget.max

        if tmin and t < tmin:
            t = tmin
        if tmax and t > tmax:
            t = tmax
        if not self.supports_seconds:
            t = t.replace(second=0)

        self.widget.value = t

        # fire handler like a UI event
        handler = getattr(self.widget, "on_change", None)
        if callable(handler):
            try:
                handler()
            except TypeError:
                handler(self.widget)

    async def wait_for_change(
        self, before: time | None, timeout: float = 2.0, interval: float = 0.05
    ):
        deadline = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < deadline:
            if self.widget.value != before:
                return
            await asyncio.sleep(interval)
        raise AssertionError("TimeInput value did not change within timeout")
