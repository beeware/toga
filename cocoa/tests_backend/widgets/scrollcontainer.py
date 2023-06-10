from toga_cocoa.libs import NSScrollView

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = NSScrollView

    @property
    def has_content(self):
        return self.native.documentView is not None

    @property
    def document_height(self):
        return self.widget.content._impl.native.bounds.size.height

    @property
    def document_width(self):
        return self.widget.content._impl.native.bounds.size.width

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass
