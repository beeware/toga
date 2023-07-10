from System.Windows.Forms import Panel

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = Panel

    def __init__(self, widget):
        super().__init__(widget)

        assert self.native.Controls.Count == 1
        self.native_content = self.native.Controls[0]
        assert isinstance(self.native_content, Panel)

    @property
    def has_content(self):
        return self.native_content.Controls.Count != 0

    @property
    def document_height(self):
        return round(self.native_content.Height / self.scale_factor)

    @property
    def document_width(self):
        return round(self.native_content.Width / self.scale_factor)

    async def scroll(self):
        self.native.VerticalScroll.Value = 100

    async def wait_for_scroll_completion(self):
        pass
