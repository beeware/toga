import pytest

from toga_cocoa.libs import (
    NSMakePoint,
    NSNotificationCenter,
    NSScrollView,
    NSScrollViewDidEndLiveScrollNotification,
    NSScrollViewDidLiveScrollNotification,
)

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = NSScrollView
    scrollbar_inset = 0
    horizontal_frame_inset = 0
    vertical_frame_inset = 0

    @property
    def has_content(self):
        return len(self.native.documentView.subviews) > 0

    @property
    def document_height(self):
        return self.native.documentView.bounds.size.height

    @property
    def document_width(self):
        return self.native.documentView.bounds.size.width

    async def scroll(self):
        if not self.native.hasVerticalScroller:
            return

        self.native.contentView.scrollToPoint(NSMakePoint(0, 600))
        self.native.reflectScrolledClipView(self.native.contentView)

        # Send 2 scroll-in-progress, then one end-scroll message.
        NSNotificationCenter.defaultCenter.postNotificationName(
            NSScrollViewDidLiveScrollNotification, object=self.native
        )
        NSNotificationCenter.defaultCenter.postNotificationName(
            NSScrollViewDidLiveScrollNotification, object=self.native
        )
        NSNotificationCenter.defaultCenter.postNotificationName(
            NSScrollViewDidEndLiveScrollNotification, object=self.native
        )

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    def assert_system_effects_top(self, expected, root):
        pytest.skip("Liquid Glass adaptation not implemented on macOS yet")
