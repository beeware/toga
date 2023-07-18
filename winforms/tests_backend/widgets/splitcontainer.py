from System.Windows.Forms import Panel, SplitContainer

from .base import SimpleProbe


class SplitContainerProbe(SimpleProbe):
    native_class = SplitContainer
    border_size = 2
    direction_change_preserves_position = True

    def __init__(self, widget):
        super().__init__(widget)

        for panel in [self.native.Panel1, self.native.Panel2]:
            assert panel.Controls.Count == 1
            assert isinstance(panel.Controls[0], Panel)

    def move_split(self, position):
        self.native.SplitterDistance = round(position * self.scale_factor)

    async def wait_for_split(self):
        pass
