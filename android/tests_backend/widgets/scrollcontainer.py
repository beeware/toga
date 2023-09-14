from android.widget import HorizontalScrollView, RelativeLayout, ScrollView

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = ScrollView
    scrollbar_inset = 0

    def __init__(self, widget):
        super().__init__(widget)

        assert self.native.getChildCount() == 1
        self.native_horizontal = self.native.getChildAt(0)
        assert isinstance(self.native_horizontal, HorizontalScrollView)

        assert self.native_horizontal.getChildCount() == 1
        self.native_content = self.native_horizontal.getChildAt(0)
        assert isinstance(self.native_content, RelativeLayout)

    @property
    def has_content(self):
        return self.native_content.getChildCount() != 0

    @property
    def document_height(self):
        return round(self.native_content.getHeight() / self.scale_factor)

    @property
    def document_width(self):
        return round(self.native_content.getWidth() / self.scale_factor)

    async def scroll(self):
        x = self.native.getWidth() * 0.5
        height = self.native.getHeight()
        await self.swipe(x, height * 0.9, x, height * 0.1)

    async def wait_for_scroll_completion(self):
        pass
