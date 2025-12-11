from PySide6.QtWidgets import QTabWidget

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = QTabWidget
    max_tabs = None
    disabled_tab_selectable = False

    def select_tab(self, index):
        # Can't select a tab that isn't visible.
        if self.native.isTabEnabled(index):
            self.native.setCurrentIndex(index)

    def tab_enabled(self, index):
        return self.native.isTabEnabled(index)

    async def wait_for_tab(self, message):
        return

    def assert_tab_icon(self, index, expected):
        # No tab icons, so if anything is returned, that's an error
        assert self.widget.content[index].icon is None
