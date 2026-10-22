import asyncio

from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe


class SplitContainerProbe(SimpleProbe):
    native_class = Gtk.Paned
    border_size = 0
    direction_change_preserves_position = False

    def move_split(self, position):
        self.native.set_position(position)

    async def wait_for_split(self):
        sub1 = self.impl.sub_containers[0]

        def size():
            if GTK_VERSION < (4, 0, 0):
                return sub1.get_allocated_height(), sub1.get_allocated_width()
            return sub1.get_height(), sub1.get_width()

        position = size()
        current = None
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = size()
