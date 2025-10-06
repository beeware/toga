from __future__ import annotations

from datetime import date, timedelta

from .base import SimpleProbe


class DateInputProbe(SimpleProbe):
    def __init__(self, widget):
        super().__init__(widget)
        self.widget = widget
        # If getattr works, we assume limits are supported.
        try:
            _ = widget.min
            _ = widget.max
            self.supports_limits = True
        except Exception:
            self.supports_limits = False

    @property
    def value(self) -> date | None:
        return self.widget.value

    @property
    def min_value(self) -> date | None:
        return self.widget.min

    @property
    def max_value(self) -> date | None:
        return self.widget.max

    async def change(self, delta_days: int):
        if callable(getattr(self, "redraw", None)):
            await self.redraw(f"DateInput change {delta_days:+d} days")

        cur = self.widget.value or date.today()
        candidate = cur + timedelta(days=int(delta_days))

        dmin, dmax = self.widget.min, self.widget.max
        if dmin and candidate < dmin:
            candidate = dmin
        if dmax and candidate > dmax:
            candidate = dmax

        self.widget.value = candidate
