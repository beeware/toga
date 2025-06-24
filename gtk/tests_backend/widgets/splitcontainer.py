import asyncio

import pytest

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class SplitContainerProbe(SimpleProbe):
    native_class = Gtk.Paned
    border_size = 0
    direction_change_preserves_position = False

    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("GTK4 doesn't split containers yet")

    def move_split(self, position):
        self.native.set_position(position)

    def repaint_needed(self):
        return (
            self.impl.sub_containers[0].needs_redraw
            or self.impl.sub_containers[1].needs_redraw
            or super().repaint_needed()
        )

    async def wait_for_split(self):
        sub1 = self.impl.sub_containers[0]
        position = sub1.get_allocated_height(), sub1.get_allocated_width()
        current = None
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = sub1.get_allocated_height(), sub1.get_allocated_width()
