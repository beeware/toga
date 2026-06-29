from PySide6.QtWidgets import QSplitter

from .base import SimpleProbe


class SplitContainerProbe(SimpleProbe):
    native_class = QSplitter
    border_size = 0
    direction_change_preserves_position = True

    def move_split(self, position):
        self.native.moveSplitter(position, 1)

    async def wait_for_split(self):
        pass
