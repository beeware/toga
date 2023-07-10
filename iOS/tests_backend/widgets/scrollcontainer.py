import asyncio

from rubicon.objc import NSMakePoint

from toga_iOS.libs import UIScrollView

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = UIScrollView
    scrollbar_inset = 0

    @property
    def has_content(self):
        return len(self.impl.document_container.native.subviews()) > 0

    @property
    def document_height(self):
        return self.native.contentSize.height

    @property
    def document_width(self):
        return self.native.contentSize.width

    async def scroll(self):
        if self.document_height <= self.height:
            return

        self.native.contentOffset = NSMakePoint(0, 600)

    async def wait_for_scroll_completion(self):
        position = self.widget.position
        current = None
        # Iterate until 2 successive reads of the scroll position,
        # 0.05s apart, return the same value
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = self.widget.position
