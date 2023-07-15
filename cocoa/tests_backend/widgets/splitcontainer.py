import asyncio

from toga_cocoa.libs import NSSplitView

from .base import SimpleProbe


class SplitContainerProbe(SimpleProbe):
    native_class = NSSplitView
    border_size = 0
    direction_change_preserves_position = False

    def move_split(self, position):
        self.native.setPosition(position, ofDividerAtIndex=0)

    async def wait_for_split(self):
        sub1 = self.impl.sub_containers[0].native.frame.size
        position = sub1.height, sub1.width
        current = None
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = sub1.height, sub1.width
