from textual.containers import Horizontal

from .base import SimpleProbe


class SwitchProbe(SimpleProbe):
    native_class = Horizontal
    minimum_required_height = 80

    def __init__(self, widget):
        super().__init__(widget)
        self.native_label = widget._impl.native_label
        self.native_switch = widget._impl.native_switch

    @property
    def text(self):
        return str(self.native_label.renderable)

    @property
    def enabled(self):
        return not self.native_switch.disabled

    @property
    def has_focus(self):
        return self.native_switch.has_focus

    async def press(self):
        self.native_switch.action_toggle_switch()
        await self.redraw("Switch should be pressed")
