from android.widget import HorizontalScrollView, ScrollView

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = ScrollView

    def __init__(self, widget):
        super().__init__(widget)

        assert self.native.getChildCount() == 1
        self.native_inner = self.native.getChildAt(0)
        assert isinstance(self.native_inner, HorizontalScrollView)

    @property
    def has_content(self):
        child_count = self.native_inner.getChildCount()
        if child_count == 0:
            return False
        elif child_count == 1:
            return True
        else:
            raise AssertionError(child_count)

    @property
    def _content(self):
        return self.native_inner.getChildAt(0)

    @property
    def document_height(self):
        return self._content.getHeight() / self.scale_factor

    @property
    def document_width(self):
        return self._content.getWidth() / self.scale_factor

    async def scroll(self):
        self.native.setScrollY(200)
        self.native_inner.setScrollX(0)

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass
