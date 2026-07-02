from textual.containers import ScrollableContainer as TextualScrollableContainer

from .base import SimpleProbe


class ScrollContainerProbe(SimpleProbe):
    native_class = TextualScrollableContainer
    scrollbar_inset = 0
    frame_inset = 0

    async def redraw(self, message=None, delay=0, wait_for=None):
        await self.widget.app._impl.wait_for_dom_operations()
        await super().redraw(message=message, delay=delay, wait_for=wait_for)
        await self.widget.app._impl.wait_for_dom_operations()

    @property
    def has_content(self):
        return self.impl.document_container.content is not None

    @property
    def document_width(self):
        return self.impl.document_width

    @property
    def document_height(self):
        return self.impl.document_height

    async def scroll(self):
        if self.impl.get_vertical():
            self.native.scroll_y = self.impl.scale_in_vertical(200)

    async def wait_for_scroll_completion(self):
        # Scroll isn't animated, so this is a no-op.
        pass
