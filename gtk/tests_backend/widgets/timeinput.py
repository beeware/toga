from datetime import time

from toga_gtk.libs import Gtk

from .base import SimpleProbe


class TimeInputProbe(SimpleProbe):
    native_class = Gtk.Box
    # Three native spin controls include six arrow buttons as well as the text.
    minimum_required_width = 400
    supports_limits = True
    supports_seconds = True

    @property
    def value(self):
        return time(*(int(field.get_text()) for field in self.impl.fields))

    @property
    def min_value(self):
        return self.impl._min_time

    @property
    def max_value(self):
        return self.impl._max_time

    async def change(self, delta):
        self.widget.focus()
        await self.redraw("Focus the time input")
        assert self.impl.has_focus
        self.impl.fields[1].spin(Gtk.SpinType.USER_DEFINED, delta)
        await self.redraw(f"Change value by {delta} minutes")
