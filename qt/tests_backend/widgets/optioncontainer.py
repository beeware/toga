from PySide6.QtWidgets import QTabWidget

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = QTabWidget
    max_tabs = None
    disabled_tab_selectable = True

    def assert_supports_content_based_rehint(self):
        pass

    def select_tab(self, index):
        self.native.setCurrentIndex(index)

    def tab_enabled(self, index):
        return self.native.isTabEnabled(index)

    async def wait_for_tab(self, message):
        return

    def assert_tab_icon(self, index, expected):
        actual = self.impl.get_option_icon(index)
        if expected is None:
            assert actual is None
        else:
            assert actual is not None
            assert actual.path.name == expected
            assert actual._impl.path.name == f"{expected}-linux.png"
