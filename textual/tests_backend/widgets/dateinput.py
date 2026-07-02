from textual.widgets import Input as TextualInput

from .base import SimpleProbe


class DateInputProbe(SimpleProbe):
    native_class = TextualInput
    minimum_required_height = 95
    supports_limits = True

    @property
    def value(self):
        return self.impl.get_value()

    @property
    def min_value(self):
        return self.impl.get_min_date()

    @property
    def max_value(self):
        return self.impl.get_max_date()

    async def change(self, delta):
        self.impl.change_by_delta(delta)
        await self.redraw(f"Change value by {delta} days")
