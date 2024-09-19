from toga_gtk.libs import Gtk

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = Gtk.Notebook
    max_tabs = None
    disabled_tab_selectable = False

    def repaint_needed(self):
        return (
            self.impl.sub_containers[self.native.get_current_page()].needs_redraw
            or super().repaint_needed()
        )

    def select_tab(self, index):
        # Can't select a tab that isn't visible.
        if self.tab_enabled(index):
            self.native.set_current_page(index)

    async def wait_for_tab(self, message):
        await self.redraw(message, delay=0.1)

    def tab_enabled(self, index):
        return self.impl.sub_containers[index].get_visible()

    def assert_tab_icon(self, index, expected):
        # No tab icons, so if anything is returned, that's an error
        assert self.widget.content[index].icon is None
