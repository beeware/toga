import pytest
from textual.widgets import TabbedContent as TextualTabbedContent

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = TextualTabbedContent
    max_tabs = None
    disabled_tab_selectable = False

    def assert_supports_content_based_rehint(self):
        pytest.xfail("Textual doesn't support content-based window rehinting.")

    def select_tab(self, index):
        if self.tab_enabled(index):
            self.impl.activate_native_tab(index)

    async def wait_for_tab(self, message):
        await self.widget.app._impl.wait_for_dom_operations()
        await self.redraw(message, delay=0.1)

    def tab_enabled(self, index):
        return self.impl.is_option_enabled(index)

    def assert_tab_icon(self, index, expected):
        assert self.widget.content[index].icon is None
