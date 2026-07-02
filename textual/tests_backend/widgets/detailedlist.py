from textual.widgets import ListView as TextualListView

from .base import SimpleProbe


class DetailedListProbe(SimpleProbe):
    native_class = TextualListView
    supports_actions = False
    supports_refresh = False

    async def redraw(self, message=None, delay=0, wait_for=None):
        await self.widget.app._impl.wait_for_dom_operations()
        await super().redraw(message=message, delay=delay, wait_for=wait_for)
        await self.widget.app._impl.wait_for_dom_operations()

    @property
    def row_count(self):
        return len(self.impl._items)

    def assert_cell_content(self, row, title, subtitle, icon=None):
        item = self.impl._items[row]
        assert item.title == title
        assert item.subtitle == subtitle
        assert item.icon is icon

    @property
    def max_scroll_position(self):
        return self.impl.max_scroll_position

    @property
    def scroll_position(self):
        return self.impl._scroll_position

    def scroll_to_top(self):
        self.widget.scroll_to_top()

    async def wait_for_scroll_completion(self):
        # Scroll isn't animated, so this is a no-op.
        pass

    async def select_row(self, row, add=False):
        self.impl.select_row(row)

    async def deselect_all(self):
        self.impl.deselect()

    def refresh_available(self):
        return False
