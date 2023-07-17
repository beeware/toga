import asyncio

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
        await self.swipe(0, -30)  # Swipe up

    async def wait_for_scroll_completion(self):
        position = self.widget.position
        current = None
        # Iterate until 2 successive reads of the scroll position,
        # 0.05s apart, return the same value
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = self.widget.position
