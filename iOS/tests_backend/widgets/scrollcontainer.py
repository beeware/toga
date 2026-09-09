import asyncio

from rubicon.objc import NSMakePoint

from toga_iOS.libs import UIScrollView

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = UIScrollView
    scrollbar_inset = 0
    frame_inset = 0

    @property
    def has_content(self):
        return len(self.impl.document_container.native.subviews()) > 0

    @property
    def document_height(self):
        document_height = self.impl.document_container.native.frame.size.height
        content_height = self.native.contentSize.height
        if self.widget.vertical:
            # A scrollable document must cover its entire scroll range so that events
            # propagate outside the original viewport; see #2411.
            assert document_height == content_height
        else:
            # On a fixed-size screen, non-scrollable content may have a minimum larger
            # than the viewport. Its native document still holds the content, while
            # contentSize remains limited to the viewport to prevent scrolling.
            assert document_height >= content_height

        return content_height

    @property
    def document_width(self):
        document_width = self.impl.document_container.native.frame.size.width
        content_width = self.native.contentSize.width
        if self.widget.horizontal:
            # A scrollable document must cover its entire scroll range so that events
            # propagate outside the original viewport; see #2411.
            assert document_width == content_width
        else:
            # See the corresponding fixed-screen case in document_height.
            assert document_width >= content_width

        return content_width

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
